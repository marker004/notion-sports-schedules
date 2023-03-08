from shared_items.utils import pp, measure_execution
from shared_items.interfaces import Notion
from requests import Response, get

from shared_items.utils import pp, measure_execution
from shared_items.interfaces import Notion

from models.soccer import GameBroadcast, GameBroadcastCollection, LeagueTypes
from shared import ElligibleSportsEnum, NotionScheduler, NotionSportsScheduleItem
from utils.assemblers import SoccerAssembler

notion = Notion()


@measure_execution("fetching new soccer schedule")
def fetch_schedule_json() -> dict:
    schedule_url = "https://www.fotmob.com/api/tvlistings?countryCode=US"
    schedule_response: Response = get(schedule_url)
    return schedule_response.json()


@measure_execution("fetching soccer leagues")
def fetch_leagues_json() -> dict:
    leagues_url = "https://www.fotmob.com/api/allLeagues"
    leagues_response: Response = get(leagues_url)
    return leagues_response.json()


def assemble_usable_games(schedule_json: dict) -> list[GameBroadcast]:
    game_broadcasts = GameBroadcastCollection(
        game_broadcasts=[
            GameBroadcast(**game_broadcast)
            for sublist in schedule_json.values()
            for game_broadcast in sublist
        ]
    )

    return game_broadcasts.usable_games()


def assemble_notion_items(
    game_broadcasts: list[GameBroadcast], league_types: LeagueTypes
) -> list[NotionSportsScheduleItem]:
    return [
        SoccerAssembler(broadcast, league_types).notion_sports_schedule_item()
        for broadcast in game_broadcasts
    ]


schedule_json = fetch_schedule_json()
leagues_json = fetch_leagues_json()
usable_games = assemble_usable_games(schedule_json)
league_types = LeagueTypes(**leagues_json)
fresh_schedule_items = assemble_notion_items(usable_games, league_types)

NotionScheduler(
    ElligibleSportsEnum.SOCCER.value, fresh_schedule_items
).schedule_them_shits()
