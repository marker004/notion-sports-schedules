from datetime import datetime, timedelta
from urllib import parse
import asyncio
from playwright.async_api import async_playwright
from shared_items.utils import pp, measure_execution, try_it

from requests import Response, get
from constants import TAB

from models.mlb import (
    MlbEspnPlusInfo,
    MlbEspnPlusInfoCollection,
    MlbResponse,
    Game as MlbGame,
)
from utils import NotionScheduler
from utils.assemblers import MlbAssembler, MlbEspnPlusAssembler

from shared import (
    ElligibleSportsEnum,
    NotionSportsScheduleItem,
    log_good_networks,
)

BOOKENDS = ["2023-03-30", "2023-10-01"]

espn_plus_url = (
    "https://www.espn.com/espnplus/catalog/b38f959b-7865-31ac-8841-b88355519e10/mlb"
)


def assemble_schedule_url() -> str:
    todays_date = datetime.today()
    end_date = todays_date + timedelta(days=45)  # note: 45 day max
    todays_date_string = todays_date.strftime("%Y-%m-%d")
    end_date_string = end_date.strftime("%Y-%m-%d")

    base_url = "https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-schedule?"

    params = (
        ("stitch_env", "prod"),
        ("sortTemplate", 5),
        ("sportId", 1),
        ("sportId", 51),
        ("startDate", todays_date_string),
        ("endDate", end_date_string),
        ("gameType", "E"),
        ("gameType", "S"),
        ("gameType", "R"),
        ("gameType", "F"),
        ("gameType", "D"),
        ("gameType", "L"),
        ("gameType", "W"),
        ("gameType", "A"),
        ("language", "en"),
        ("leagueId", 104),
        ("leagueId", 103),
        ("leagueId", 160),
        ("contextTeamId", ""),
    )

    return base_url + parse.urlencode(params)


@measure_execution(f"{TAB}fetching new MLB schedule")
def fetch_schedule_json() -> dict:
    url = assemble_schedule_url()
    schedule_response: Response = get(url)
    return schedule_response.json()


async def fetch_espn_plus_schedule_response() -> tuple[list[str], list[str], list[str]]:
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        await page.goto(espn_plus_url, wait_until="networkidle", timeout=0)

        items = await page.query_selector_all(".Carousel")

        first_carousel = items[0]

        matchups_html = await first_carousel.query_selector_all(".WatchTile__Title")
        channels_html = await first_carousel.query_selector_all(".WatchTile__Meta")
        times_html = await first_carousel.query_selector_all(".MediaPlaceholder__Pill")

        matchups = [await matchup.inner_text() for matchup in matchups_html]
        channels = [await channel.inner_text() for channel in channels_html]
        times = [await time.inner_text() for time in times_html]

        game_infos = (times, matchups, channels)

        await browser.close()

        return game_infos


def assemble_usable_events(schedule_json: dict) -> list[MlbGame]:
    mlb_response = MlbResponse(**schedule_json)
    return mlb_response.usable_events()


def assemble_usable_espn_plus_games(
    response: tuple[list[str], list[str], list[str]]
) -> list[MlbEspnPlusInfo]:
    collection = MlbEspnPlusInfoCollection(
        games=[
            MlbEspnPlusInfo(matchup=matchup, channel=channel, time=time)
            for time, matchup, channel in zip(*response)
        ]
    )

    return collection.usable_events()


def assemble_notion_items(games: list[MlbGame]) -> list[NotionSportsScheduleItem]:
    return [MlbAssembler(game).notion_sports_schedule_item() for game in games]


def assemble_espn_plus_notion_items(
    games: list[MlbEspnPlusInfo],
) -> list[NotionSportsScheduleItem]:
    return [MlbEspnPlusAssembler(game).notion_sports_schedule_item() for game in games]


@try_it
def schedule_mlb():
    schedule_json = fetch_schedule_json()
    usable_events = assemble_usable_events(schedule_json)
    fresh_items = assemble_notion_items(usable_events)

    espn_plus_response = asyncio.run(fetch_espn_plus_schedule_response())
    usable_espn_plus_games = assemble_usable_espn_plus_games(espn_plus_response)
    fresh_espn_plus_items = assemble_espn_plus_notion_items(usable_espn_plus_games)

    combined_games = fresh_items + fresh_espn_plus_items

    log_good_networks(combined_games)

    NotionScheduler(ElligibleSportsEnum.MLB.value, combined_games).schedule()


if __name__ == "__main__":
    schedule_mlb()
