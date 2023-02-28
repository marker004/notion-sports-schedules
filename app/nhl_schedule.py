from datetime import datetime
from urllib import parse

from models.nhl import LeagueBroadcastSchedule
from shared_items.utils import pp, measure_execution
from shared_items.interfaces import Notion
from requests import Response, get

from shared import (
    ElligibleSportsEnum,
    clear_db_for_sport,
    insert_to_database,
)
from utils.assemblers import NhlAssembler

print("no real need to run this. nearly every out of market game is available on 'NHL Power Play on ESPN+'")

BOOKENDS = ["2022-10-07", "2023-4-13"]

base_url = "https://statsapi.web.nhl.com/api/v1/schedule?"

todays_date = datetime.today().strftime("%Y-%m-%d")

params = (
    ("startDate", todays_date),
    ("endDate", BOOKENDS[1]),
    ("hydrate", "broadcasts(all)"),
    ("site", "en_nhl"),
    ("teamId", ""),
    ("gameType", ""),
    ("timecode", ""),
)

assembled_url = base_url + parse.urlencode(params, safe=",()")

notion = Notion()

schedule_response: Response = get(assembled_url)
schedule_json: dict = schedule_response.json()

league_broadcast_schedule = LeagueBroadcastSchedule(**schedule_json)

usable_games = league_broadcast_schedule.usable_games()

assembed_items = [
    NhlAssembler(game).notion_sports_schedule_item() for game in usable_games
]

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembed_items
]


@measure_execution("deleting existing NHL games")
def delete_existing_games():
    clear_db_for_sport(ElligibleSportsEnum.NHL.value)


delete_existing_games()


@measure_execution("inserting NHL games")
def insert_games():
    insert_to_database(all_props)


insert_games()
