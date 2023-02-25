from requests import get, Response

from shared_items.interfaces.notion import Notion
from shared_items.utils import measure_execution

from models.nba import Game, LeagueSchedule

from shared import SCHEDULE_DATABASE_ID, ElligibleSportsEnum, beginning_of_today, fetch_all_games_by_sport, fetch_only_future_games_by_sport
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

@measure_execution('deleting existing NBA games')
def clear_db_totally():
    fetch_only_nba_games = fetch_all_games_by_sport(ElligibleSportsEnum.NBA.value)
    delete_nba_games = notion.recursive_fetch_and_delete(fetch_only_nba_games)
    delete_nba_games()

# deleting_start_time = time.time()
# print("deleting existing NBA games")
clear_db_totally()
# print(f"Done. Took {time.time() - deleting_start_time} seconds")


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

@measure_execution('inserting NBA games')
def insert_games():
    for props in all_props:
        notion.client.pages.create(
            parent={"database_id": SCHEDULE_DATABASE_ID}, properties=props
        )
