from datetime import datetime
from urllib import parse

from models.nhl import LeagueBroadcastSchedule
from shared_items.utils import pp, measure_execution
from shared_items.interfaces import Notion
from requests import Response, get
from models.nhl_espn import DailyEspnPlusNhlSchedule

from shared import (
    ElligibleSportsEnum,
    clear_db_for_sport,
    insert_to_database,
)
from utils.assemblers import NhlAssembler, NhlEspnPlusAssembler

notion = Notion()


BOOKENDS = ["2022-10-07", "2023-4-13"]

league_schedule_base_url = "https://statsapi.web.nhl.com/api/v1/schedule?"

todays_date = datetime.today().strftime("%Y-%m-%d")

league_schedule_params = (
    ("startDate", todays_date),
    ("endDate", BOOKENDS[1]),
    ("hydrate", "broadcasts(all)"),
    ("site", "en_nhl"),
    ("teamId", ""),
    ("gameType", ""),
    ("timecode", ""),
)

assembled_league_schedule_url = league_schedule_base_url + parse.urlencode(
    league_schedule_params, safe=",()"
)

power_play_schedule_base_url = (
    "https://site.web.api.espn.com/apis/v2/scoreboard/header?"
)

power_play_schedule_params = (
    ("sport", "hockey"),
    ("league", "nhl"),
    ("region", "us"),
    ("lang", "en"),
    ("contentorigin", "espn"),
    ("buyWindow", "1m"),
    ("showAirings", "buy,live,replay"),
    ("showZipLookup", "true"),
    ("tz", "America/Indianapolis"),
)
assembled_power_play_schedule_url = power_play_schedule_base_url + parse.urlencode(
    power_play_schedule_params
)
power_play_schedule_response: Response = get(assembled_power_play_schedule_url)
power_play_schedule_json: dict = power_play_schedule_response.json()


power_play_nhl_schedule = DailyEspnPlusNhlSchedule(**power_play_schedule_json)

usable_power_play_games = power_play_nhl_schedule.usable_games()

assembled_power_play_items = [
    NhlEspnPlusAssembler(game).notion_sports_schedule_item()
    for game in usable_power_play_games
]

schedule_response: Response = get(assembled_league_schedule_url)
schedule_json: dict = schedule_response.json()

league_broadcast_schedule = LeagueBroadcastSchedule(**schedule_json)


usable_games = league_broadcast_schedule.usable_games()


assembled_items = [
    NhlAssembler(game).notion_sports_schedule_item() for game in usable_games
]

# assuming there's no overlap between national and regional broadcast games
# and non-blacked out out of market games. can uniq if need be
combined_games = sorted(
    assembled_items + assembled_power_play_items, key=lambda x: x.date
)

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in combined_games
]


@measure_execution("deleting existing NHL games")
def delete_existing_games():
    clear_db_for_sport(ElligibleSportsEnum.NHL.value)


delete_existing_games()


@measure_execution("inserting NHL games")
def insert_games():
    insert_to_database(all_props)


insert_games()
