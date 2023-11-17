from requests import get, Response

from shared_items.utils import measure_execution, try_it
from constants import TAB

from models.nba import LeagueSchedule, Game as NbaGame

from shared import ElligibleSportsEnum, NotionSportsScheduleItem, log_good_networks
from utils import NotionScheduler
from utils.assemblers import NbaAssembler

YEAR = 2023


@measure_execution(f"{TAB}fetching new NBA schedule")
def fetch_schedule_json() -> dict:
    url_2022_2023_schedule = f"https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{YEAR}/league/00_full_schedule.json"
    schedule_response: Response = get(url_2022_2023_schedule)
    return schedule_response.json()


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

    log_good_networks(fresh_items)

    NotionScheduler(ElligibleSportsEnum.NBA.value, fresh_items).schedule()

if (__name__ == "__main__"):
    schedule_nba()