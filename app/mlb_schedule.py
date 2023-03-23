from datetime import datetime, timedelta
from urllib import parse
from shared_items.interfaces.notion import Notion
from shared_items.utils import pp, measure_execution

from requests import Response, get

from models.mlb import MlbResponse, Game as MlbGame
from utils.assemblers import MlbAssembler

from shared import ElligibleSportsEnum, NotionScheduler, NotionSportsScheduleItem

notion = Notion()

BOOKENDS = ["2023-03-30", "2023-10-01"]


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
        ("gameType", "F"),
        ("gameType", "D"),
        ("gameType", "L"),
        ("gameType", "W"),
        ("gameType", "A"),
        ("gameType", "S"),  # spring training
        ("gameType", "R"),  # regular season
        ("language", "en"),
        ("leagueId", 104),
        ("contextTeamId", ""),
        ("hydrate", "broadcasts"),
    )

    return base_url + parse.urlencode(params)


@measure_execution("fetching new MLB schedule")
def fetch_schedule_json() -> dict:
    url = assemble_schedule_url()
    schedule_response: Response = get(url)
    return schedule_response.json()


def assemble_usable_games(schedule_json: dict) -> list[MlbGame]:
    mlb_response = MlbResponse(**schedule_json)
    return mlb_response.usable_games()


def assemble_notion_items(games: list[MlbGame]) -> list[NotionSportsScheduleItem]:
    return [MlbAssembler(game).notion_sports_schedule_item() for game in games]


schedule_json = fetch_schedule_json()
usable_games = assemble_usable_games(schedule_json)
fresh_items = assemble_notion_items(usable_games)


all_good_networks = []
for item in fresh_items:
    all_good_networks.append(item.network)

print(set(all_good_networks))

NotionScheduler(ElligibleSportsEnum.MLB.value, fresh_items).schedule_them_shits()
