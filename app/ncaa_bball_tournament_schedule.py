from requests import Response, get
from shared_items.utils import pp, measure_execution, try_it
from constants import TAB

from models.ncaa_bball import Game as NcaaGame, GameCollection
from shared import ElligibleSportsEnum, NotionSportsScheduleItem, log_good_networks
from utils import NotionScheduler
from utils.assemblers import NcaaTournamentAssembler


def assemble_league_schedule_url() -> str:
    return "https://sdataprod.ncaa.com/?operationName=scores_bracket_web&variables=%7B%22seasonYear%22%3A2022%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22f21cac8420a55a7d190f2f686a441e2507d8fb80f25eac5c91131ddd9df588da%22%7D%7D"


@measure_execution(f"{TAB}fetching new tourney schedule")
def fetch_schedule_json() -> dict:
    url = assemble_league_schedule_url()
    schedule_response: Response = get(url)
    return schedule_response.json()


def assemble_usable_events(schedule_json: dict) -> list[NcaaGame]:
    return GameCollection(games=schedule_json["data"]["mmlContests"]).usable_events()


def assemble_notion_items(games: list[NcaaGame]) -> list[NotionSportsScheduleItem]:
    return [
        NcaaTournamentAssembler(game).notion_sports_schedule_item() for game in games
    ]

@try_it
def schedule_march_madness():
    schedule_json = fetch_schedule_json()
    usable_events = assemble_usable_events(schedule_json)
    fresh_games = assemble_notion_items(usable_events)

    log_good_networks(fresh_games)

    NotionScheduler(ElligibleSportsEnum.BASKETBALL.value, fresh_games).schedule()

if (__name__ == "__main__"):
    schedule_march_madness()