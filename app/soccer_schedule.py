from shared_items.utils import pp
from shared_items.interfaces import Notion
from requests import Response, get

from models.soccer import GameBroadcast, Matches
from shared import SCHEDULE_DATABASE_ID, NotionSportsScheduleItem

notion = Notion()

schedule_url = "https://www.fotmob.com/api/tvlistings?countryCode=US"
matches_url = "https://www.fotmob.com/api/matches?date=20230216&timezone=America%2FIndianapolis&ccode3=USA_IN"

schedule_response: Response = get(schedule_url)
matches_response: Response = get(matches_url)


schedule_json: dict = schedule_response.json()
matches_json: dict = matches_response.json()


game_broadcasts: list[GameBroadcast] = [
    GameBroadcast(**game_broadcast)
    for sublist in schedule_json.values()
    for game_broadcast in sublist
]

matches = Matches.parse_obj(matches_json)

BROADCAST_BADLIST = [
    "Antenna 20 Years",
    # 'CBS',
    # 'CBS Sports Network',
    # 'CBS Sports Network HD',
    "CL beIN Sports English SD in Spanish",
    "ESPN Deportes",
    "ESPN Deportes HD",
    # 'ESPN+ USA',
    "ESPN3",
    # 'FS2',
    "Fox Deportes",
    "Fox Deportes HD",
    "Fox Soccer Plus",
    "Fox Soccer Plus HD",
    "Fox Sports 2 HD",
    "GOL TV",
    # 'NBC',
    "NBC Sports California SAT",
    "NBC Sports California SAT HD",
    # 'NBC Sports Chicago',
    # 'NBC Sports Chicago HD',
    "NBCSports.com",
    "Nuestra Tele Internacional",
    # 'Paramount+',
    # 'Peacock',
    "RREC",
    "SporTV",
    # 'TNT',
    # 'TNT HD',
    # 'TNT HD (Pacific)',
    "TUDN",
    "TV5MONDE Etats Unis",
    "Telemundo Satellite Feed",
    "Telemundo Satellite Feed Pacific",
    # 'Telemundo Television Network',
    "Twitch",
    "TyC Sports Internacional USA",
    # 'UNIVERSO',
    # 'UNIVERSO HD',
    # 'USA Network',
    # 'USA Network HD',
    "UniMas",
    "UniMas Satellite Feed (Pacific)",
    "Univision NOW",
    "Univision Network",
    "VIX+",
    "ViX",
    "Yes Network",
    "Yes Network HD",
    "beIN Sports",
    "beIN Sports En Español",
    "beIN Sports En Español HD",
    "beIN Sports HD",
    "iFollow",
]

broadcasts = [
    broadcast
    for broadcast in game_broadcasts
    if broadcast.station.name not in BROADCAST_BADLIST and "live" in broadcast.tags
]

# todo: uniq this list of broadcasts


def assemble_matchup(broadcast: GameBroadcast) -> str:
    teams = sorted(broadcast.program.teams, key=lambda t: t.isHome, reverse=True)
    team_names = [team.name for team in teams]
    return " vs ".join(team_names)


def format_date(broadcast: GameBroadcast) -> str:
    return broadcast.startTime.strftime("%Y-%m-%dT%H:%M:%S")


def format_network(broadcast: GameBroadcast) -> str:
    return broadcast.station.name


def fetch_league(broadcast: GameBroadcast, matches: Matches) -> str:
    return next(
        (league.name for league in matches.leagues if league.id == broadcast.leagueId),
        "",
    )


def format_sport() -> str:
    return "⚽"


broadcasts.sort(key=lambda b: b.startTime)

schedule_items = [NotionSportsScheduleItem(
        matchup=assemble_matchup(broadcast),
        date=format_date(broadcast),
        network=format_network(broadcast),
        league=fetch_league(broadcast, matches),
        sport=format_sport(),
    ) for broadcast in broadcasts]

for schedule_item in schedule_items:
    props = notion.assemble_props(schedule_item.format_for_notion_interface())

    # don't do this until deduped and deletion in place
    # notion.client.pages.create(
    #     parent={"database_id": SCHEDULE_DATABASE_ID}, properties=props
    # )