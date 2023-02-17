from datetime import time, datetime
from pprint import pp
from typing import Any, cast
from requests import get, Response

from shared_items.interfaces.notion import Notion

from models.nba import Game, LeagueSchedule

from shared import SCHEDULE_DATABASE_ID
from utils.assemblers import NbaAssembler

# SEASON_DATE_BOOKENDS = ["2022-10-18", "2023-06-18"]

notion = Notion()

YEAR = 2022
url_2022_2023_schedule = f"https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{YEAR}/league/00_full_schedule.json"


print("fetching schedule...")
response: Response = get(url_2022_2023_schedule)
schedule: dict = response.json()
print("done")

league_schedule = LeagueSchedule(
    month_schedule=[month["mscd"] for month in schedule["lscd"]]
)

beginning_of_today = datetime.combine(datetime.now(), time())


def fetch_only_future_basketball_games(next_cursor=None):
    filter = {
        "and": [
            {
                "property": "Date",
                "date": {
                    "on_or_after": beginning_of_today.strftime("%Y-%m-%dT%H:%M:%S")
                },
            },
            {
                "property": "Sport",
                "rich_text": {"equals": "🏀"},
            },
        ]
    }
    return notion.client.databases.query(
        database_id=SCHEDULE_DATABASE_ID, filter=filter, next_cursor=next_cursor
    )


def recursive_fetch_and_delete(next_cursor=None):
    database_response = cast(Any, fetch_only_future_basketball_games(next_cursor))
    database_rows = database_response["results"]

    for row in database_rows:
        notion.client.blocks.delete(block_id=row["id"])

    if database_response["has_more"]:
        recursive_fetch_and_delete(database_response["next_cursor"])


def clear_db_totally():
    recursive_fetch_and_delete()


print("deleting existing games starting after yesterday...")
clear_db_totally()
print("Done")


watchable_games: list[Game] = [
    game
    for month in league_schedule.month_schedule
    for game in month.games
    if game.eastern_time > beginning_of_today and game.watchable()
]

assembed_items = [
    NbaAssembler(game).notion_sports_schedule_item() for game in watchable_games
]

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembed_items
]

print("inserting games starting after yesterday...")
for props in all_props:
    notion.client.pages.create(
        parent={"database_id": SCHEDULE_DATABASE_ID}, properties=props
    )
print("Done")
