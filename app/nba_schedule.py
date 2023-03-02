from requests import get, Response

from shared_items.interfaces.notion import Notion
from shared_items.utils import measure_execution

from models.nba import LeagueSchedule

from shared import (
    ElligibleSportsEnum,
    clear_db_for_sport,
    insert_to_database,
)
from utils.assemblers import NbaAssembler

# SEASON_DATE_BOOKENDS = ["2022-10-18", "2023-06-18"]

notion = Notion()

YEAR = 2022
url_2022_2023_schedule = f"https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{YEAR}/league/00_full_schedule.json"


response: Response = get(url_2022_2023_schedule)
schedule: dict = response.json()

league_schedule = LeagueSchedule(
    month_schedule=[month["mscd"] for month in schedule["lscd"]]
)

usable_games = league_schedule.usable_games()

assembled_items = [
    NbaAssembler(game).notion_sports_schedule_item() for game in usable_games
]

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembled_items
]


@measure_execution("deleting existing NBA games")
def delete_existing_games():
    clear_db_for_sport(ElligibleSportsEnum.NBA.value)


delete_existing_games()


@measure_execution("inserting NBA games")
def insert_games():
    insert_to_database(all_props)


insert_games()
