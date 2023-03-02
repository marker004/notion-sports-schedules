from datetime import datetime, timedelta
from urllib import parse
from shared_items.interfaces.notion import Notion
from shared_items.utils import pp, measure_execution

from requests import Response, get

from models.mlb import MlbResponse
from utils.assemblers import MlbAssembler

from shared import (
    ElligibleSportsEnum,
    clear_db_for_sport,
    insert_to_database,
)


BOOKENDS = ["2023-03-30", "2023-10-01"]

notion = Notion()

# note: 45 day max
todays_date = datetime.today()
end_date = todays_date + timedelta(days=45)
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

assembled_url = base_url + parse.urlencode(params)

schedule_response: Response = get(assembled_url)
schedule_json: dict = schedule_response.json()

mlb_response = MlbResponse(**schedule_json)

usable_games = mlb_response.usable_games()

assembled_items = [
    MlbAssembler(game).notion_sports_schedule_item() for game in usable_games
]

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembled_items
]


@measure_execution("deleting existing MLB games")
def delete_existing_games():
    clear_db_for_sport(ElligibleSportsEnum.MLB.value)


delete_existing_games()


@measure_execution("inserting MLB games")
def insert_games():
    insert_to_database(all_props)


insert_games()
