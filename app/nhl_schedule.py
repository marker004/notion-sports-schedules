from datetime import datetime
from urllib import parse
from requests import Response, get

from shared_items.utils import pp, measure_execution

from models.nhl import LeagueBroadcastSchedule, Game as LeagueGame
from models.nhl_espn import DailyEspnPlusNhlSchedule, Event as PowerPlayGame
from shared import ElligibleSportsEnum, NotionSportsScheduleItem
from utils import NotionScheduler
from utils.assemblers import NhlAssembler, NhlEspnPlusAssembler

BOOKENDS = ["2022-10-07", "2023-4-13"]


def assemble_league_schedule_url() -> str:
    league_schedule_base_url = "https://statsapi.web.nhl.com/api/v1/schedule?"
    todays_date = datetime.today().strftime("%Y-%m-%d")
    league_schedule_params = (
        ("startDate", todays_date),
        ("endDate", "2023-6-30"),
        ("hydrate", "broadcasts(all)"),
        ("site", "en_nhl"),
        ("teamId", ""),
        ("gameType", ""),
        ("timecode", ""),
    )
    return league_schedule_base_url + parse.urlencode(
        league_schedule_params, safe=",()"
    )


def assemble_power_play_schedule_url() -> str:
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
    return power_play_schedule_base_url + parse.urlencode(power_play_schedule_params)


@measure_execution("fetching new NHL schedule")
def fetch_schedule_json() -> dict:
    url = assemble_league_schedule_url()
    schedule_response: Response = get(url)
    return schedule_response.json()


@measure_execution("fetching new NHL PowerPlay schedule")
def fetch_power_play_json() -> dict:
    url = assemble_power_play_schedule_url()
    power_play_schedule_response: Response = get(url)
    return power_play_schedule_response.json()


def assemble_usable_games() -> list[LeagueGame]:
    league_broadcast_schedule = LeagueBroadcastSchedule(**schedule_json)
    return league_broadcast_schedule.usable_games()


def assemble_usable_power_play_games() -> list[PowerPlayGame]:
    power_play_nhl_schedule = DailyEspnPlusNhlSchedule(**power_play_schedule_json)
    return power_play_nhl_schedule.usable_games()


def assemble_notion_items(
    league_games: list[LeagueGame], power_play_games: list[PowerPlayGame]
) -> list[NotionSportsScheduleItem]:
    assembled_items = [
        NhlAssembler(game).notion_sports_schedule_item() for game in league_games
    ]
    assembled_power_play_items = [
        NhlEspnPlusAssembler(game).notion_sports_schedule_item()
        for game in power_play_games
    ]
    return sorted(assembled_items + assembled_power_play_items, key=lambda x: x.date)


schedule_json = fetch_schedule_json()
power_play_schedule_json = fetch_power_play_json()
usable_games = assemble_usable_games()
usable_power_play_games = assemble_usable_power_play_games()
combined_items = assemble_notion_items(usable_games, usable_power_play_games)

NotionScheduler(ElligibleSportsEnum.NHL.value, combined_items).schedule_them_shits()
