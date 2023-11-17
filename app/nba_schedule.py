import asyncio
from requests import get, Response
from playwright.async_api import async_playwright

from shared_items.utils import measure_execution, try_it
from shared import beginning_of_today
from datetime import datetime
from dateutil.tz import tzlocal
from constants import TAB

from models.nba import HboMaxGame, HboMaxGameInfo, LeagueSchedule, Game as NbaGame

from shared import ElligibleSportsEnum, NotionSportsScheduleItem, log_good_networks
from utils import NotionScheduler
from utils.assemblers import HboMaxGameAssembler, NbaAssembler
from bs4 import BeautifulSoup, Tag


YEAR = 2023


@measure_execution(f"{TAB}fetching new NBA schedule")
def fetch_schedule_json() -> dict:
    url_2022_2023_schedule = f"https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{YEAR}/league/00_full_schedule.json"
    schedule_response: Response = get(url_2022_2023_schedule)
    return schedule_response.json()


async def fetch_hbo_max_schedule_response() -> list[str]:
    if beginning_of_today > datetime(2024, 2, 24).astimezone(tzlocal()):
        raise Exception("HBO Max NBA games are only available until 2/24/2024")

    hbo_max_url = "https://www.max.com/sports/nba"

    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        await page.goto(hbo_max_url, wait_until="networkidle")

        selector = ".event-container"
        items = await page.query_selector_all(selector)
        game_infos = [await item.inner_html() for item in items]

        await browser.close()

        return game_infos


def assemble_usable_hbo_max_games(game_infos: list[str]) -> list[HboMaxGame]:
    relevant_game_info = []

    for info in game_infos:
        soup = BeautifulSoup(info, "html.parser")
        title = soup.find("h6", class_="event-full-title")
        network = soup.find("p", class_="event-short-title")
        time = soup.find("p", class_="date-time")

        if (
            isinstance(title, Tag)
            and isinstance(time, Tag)
            and isinstance(network, Tag)
        ):
            relevant_game_info.append(
                HboMaxGameInfo(
                    {
                        "matchup": title.text,
                        "datetime": time.text,
                        "network": network.text,
                    }
                )
            )

    return [HboMaxGame(**info) for info in relevant_game_info]


def assemble_hbo_max_notion_items(
    games: list[HboMaxGame],
) -> list[NotionSportsScheduleItem]:
    return [HboMaxGameAssembler(game).notion_sports_schedule_item() for game in games]


def assemble_usable_events(schedule_json: dict) -> list[NbaGame]:
    league_schedule = LeagueSchedule(
        month_schedule=[month["mscd"] for month in schedule_json["lscd"]]
    )

    return league_schedule.usable_events()


def assemble_notion_items(games: list[NbaGame]) -> list[NotionSportsScheduleItem]:
    return [NbaAssembler(game).notion_sports_schedule_item() for game in games]


@try_it
def schedule_nba():
    schedule_json = fetch_schedule_json()
    usable_events = assemble_usable_events(schedule_json)
    fresh_items = assemble_notion_items(usable_events)

    hbo_max_response = asyncio.run(fetch_hbo_max_schedule_response())
    usable_hbo_max_games = assemble_usable_hbo_max_games(hbo_max_response)
    fresh_hbo_max_items = assemble_hbo_max_notion_items(usable_hbo_max_games)

    combined_games = fresh_items + fresh_hbo_max_items

    log_good_networks(combined_games)

    NotionScheduler(ElligibleSportsEnum.NBA.value, combined_games).schedule()


if __name__ == "__main__":
    schedule_nba()
