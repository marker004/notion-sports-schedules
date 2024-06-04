import asyncio
from playwright.async_api import async_playwright
from constants import TAB

from models.soccer import AppleTVFreeSoccer
from shared import AppleTVGameInfo, NotionSportsScheduleItem, log_good_networks
from utils.assemblers import AppleTVFreeGamesSoccerAssembler
from requests import Response, get

from shared_items.utils import pp, measure_execution, try_it

from models.soccer import GameBroadcast, GameBroadcastCollection, LeagueTypes
from shared import ElligibleSportsEnum, NotionSportsScheduleItem
from utils import NotionScheduler
from utils.assemblers import SoccerAssembler

apple_url = "https://tv.apple.com/us/collection/free-matches/edt.col.63e868dd-8b2a-4a50-9cf5-0bd992c03f20"


@measure_execution(f"{TAB}fetching new soccer schedule")
def fetch_schedule_json() -> dict:
    schedule_url = "https://www.fotmob.com/api/tvlistings?countryCode=US"
    schedule_response: Response = get(schedule_url)
    return schedule_response.json()


async def fetch_apple_tv_schedule_response() -> list[str]:
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        await page.goto(apple_url, wait_until="networkidle")

        selector = ".collection-page__item"
        items = await page.query_selector_all(selector)
        game_infos = [await item.inner_text() for item in items]

        await browser.close()

        return game_infos


@measure_execution(f"{TAB}fetching soccer leagues")
def fetch_leagues_json() -> dict:
    leagues_url = "https://www.fotmob.com/api/allLeagues"
    leagues_response: Response = get(leagues_url)
    return leagues_response.json()


def assemble_usable_events(schedule_json: dict) -> list[GameBroadcast]:
    game_broadcast_collection = GameBroadcastCollection(
        game_broadcasts=[
            GameBroadcast(**game_broadcast)
            for sublist in schedule_json.values()
            for game_broadcast in sublist
        ]
    )

    return game_broadcast_collection.usable_events()


def assemble_usable_apple_tv_games(response: list[str]) -> list[AppleTVFreeSoccer]:
    split = [
        [string for string in game_info.split("\n") if string] for game_info in response
    ]

    named_game_info = [
        AppleTVGameInfo(relative_date, matchup, league)
        for relative_date, matchup, league in split
    ]
    return [AppleTVFreeSoccer(**info._asdict()) for info in named_game_info]


def assemble_notion_items(
    game_broadcasts: list[GameBroadcast], league_types: LeagueTypes
) -> list[NotionSportsScheduleItem]:
    return [
        SoccerAssembler(broadcast, league_types).notion_sports_schedule_item()
        for broadcast in game_broadcasts
    ]


def assemble_apple_tv_notion_items(
    games: list[AppleTVFreeSoccer],
) -> list[NotionSportsScheduleItem]:
    return [
        AppleTVFreeGamesSoccerAssembler(game).notion_sports_schedule_item()
        for game in games
    ]


@try_it
def schedule_soccer():
    schedule_json = fetch_schedule_json()
    leagues_json = fetch_leagues_json()
    usable_events = assemble_usable_events(schedule_json)
    league_types = LeagueTypes(**leagues_json)
    fresh_schedule_items = assemble_notion_items(usable_events, league_types)

    apple_tv_response = asyncio.run(fetch_apple_tv_schedule_response())
    usable_apple_tv_games = assemble_usable_apple_tv_games(apple_tv_response)
    fresh_apple_tv_items = assemble_apple_tv_notion_items(usable_apple_tv_games)

    combined_games = fresh_schedule_items + fresh_apple_tv_items

    log_good_networks(combined_games)

    NotionScheduler(ElligibleSportsEnum.SOCCER.value, combined_games).schedule()


if __name__ == "__main__":
    schedule_soccer()
