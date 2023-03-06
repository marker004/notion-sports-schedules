from typing import Optional
from shared_items.utils import pp, measure_execution
from shared_items.interfaces import Notion
from requests import Response, get

from models.soccer import GameBroadcast, GameBroadcastCollection, LeagueTypes
from shared import (
    ElligibleSportsEnum,
    NotionSportsScheduleItem,
    clear_db_for_sport,
    fetch_all_games_by_sport,
    insert_to_database,
)
from utils.assemblers import SoccerAssembler


notion = Notion()

schedule_url = "https://www.fotmob.com/api/tvlistings?countryCode=US"
leagues_url = "https://www.fotmob.com/api/allLeagues"

schedule_response: Response = get(schedule_url)
schedule_json: dict = schedule_response.json()

leagues_response: Response = get(leagues_url)
leagues_json: dict = leagues_response.json()

league_types = LeagueTypes(**leagues_json)

game_broadcasts = GameBroadcastCollection(
    game_broadcasts=[
        GameBroadcast(**game_broadcast)
        for sublist in schedule_json.values()
        for game_broadcast in sublist
    ]
)

usable_games = game_broadcasts.usable_games()

assembled_items = [
    SoccerAssembler(broadcast, league_types).notion_sports_schedule_item()
    for broadcast in usable_games
]


all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembled_items
]


def fetch_all_existing_notion_games() -> list[dict]:
    game_fetcher = fetch_all_games_by_sport(ElligibleSportsEnum.SOCCER.value)

    all_games: list[dict] = []
    next_cursor: Optional[str] = None

    while True:
        response = game_fetcher(next_cursor)
        next_cursor = response["next_cursor"]
        all_games += response["results"]
        if not response["has_more"]:
            break

    return all_games


# NotionSportsScheduleItem
all_existing_notion_games = fetch_all_existing_notion_games()

# import pdb; pdb.set_trace()
existing_schedule_items = [
    NotionSportsScheduleItem.from_notion_interface(notion_game['properties'])
    for notion_game in all_existing_notion_games
]

delete_list = set(existing_schedule_items) - set(assembled_items)
do_nothing_list = list(set(assembled_items) & set(existing_schedule_items))
add_list = set(assembled_items) - set(existing_schedule_items)

# note: https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python

import pdb

pdb.set_trace()


# @measure_execution("deleting existing soccer games")
# def delete_existing_games():
#     clear_db_for_sport(ElligibleSportsEnum.SOCCER.value)


# delete_existing_games()


# @measure_execution("inserting soccer games")
# def insert_games():
#     insert_to_database(all_props)


# insert_games()
