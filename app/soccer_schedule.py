from itertools import groupby
from shared_items.utils import pp
from shared_items.interfaces import Notion
from requests import Response, get
from constants import SOCCER_BROADCAST_BADLIST

from models.soccer import GameBroadcast, LeagueTypes
from shared import SCHEDULE_DATABASE_ID
from utils.assemblers import SoccerAssembler

notion = Notion()

schedule_url = "https://www.fotmob.com/api/tvlistings?countryCode=US"
leagues_url = "https://www.fotmob.com/api/allLeagues"

schedule_response: Response = get(schedule_url)
schedule_json: dict = schedule_response.json()

leagues_response: Response = get(leagues_url)
leagues_json: dict = leagues_response.json()

league_types = LeagueTypes(**leagues_json)

game_broadcasts: list[GameBroadcast] = [
    GameBroadcast(**game_broadcast)
    for sublist in schedule_json.values()
    for game_broadcast in sublist
]

broadcasts = [
    broadcast
    for broadcast in game_broadcasts
    if broadcast.station.name not in SOCCER_BROADCAST_BADLIST
    and "live" in broadcast.tags
]


broadcasts.sort(key=lambda b: b.startTime)


def unique_broadcasts_by_match_id(
    broadcasts: list[GameBroadcast],
) -> list[GameBroadcast]:
    broadcast_groups: list[list[GameBroadcast]] = []
    uniquekeys = []

    for k, v in groupby(broadcasts, key=lambda b: b.matchId):
        broadcast_groups.append(list(v))
        uniquekeys.append(k)

    unique_broadcasts: list[GameBroadcast] = []
    for broadcast_group in broadcast_groups:
        first_broadcast = broadcast_group[0]
        networks: list[str] = []
        for broadcast in broadcast_group:
            networks.append(broadcast.station.name)
        first_broadcast.station.name = ", ".join(networks)
        unique_broadcasts.append(first_broadcast)
    return unique_broadcasts


unique_broadcasts = unique_broadcasts_by_match_id(broadcasts)


assembed_items = [
    SoccerAssembler(broadcast, league_types).notion_sports_schedule_item()
    for broadcast in unique_broadcasts
]


all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembed_items
]

pp(all_props)

exit()

for props in all_props:
    notion.client.pages.create(
        parent={"database_id": SCHEDULE_DATABASE_ID}, properties=props
    )
