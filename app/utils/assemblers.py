from abc import ABC
from zoneinfo import ZoneInfo
from models.soccer import GameBroadcast, LeagueTypes
from models.nba import Game as NbaGame
from shared import ElligibleSportsEnum, NotionSportsScheduleItem


class Assembler(ABC):
    def assemble_matchup(self) -> str:
        raise NotImplementedError

    def format_date(self) -> str:
        raise NotImplementedError

    def format_network(self) -> str:
        raise NotImplementedError

    def fetch_league(self) -> str:
        raise NotImplementedError

    def format_sport(self) -> str:
        raise NotImplementedError

    def notion_sports_schedule_item(self) -> NotionSportsScheduleItem:
        return NotionSportsScheduleItem(
            matchup=self.assemble_matchup(),
            date=self.format_date(),
            network=self.format_network(),
            league=self.fetch_league(),
            sport=self.format_sport(),
        )


class NbaAssembler(Assembler):
    def __init__(self, game: NbaGame):
        self.game = game

    def assemble_matchup(self) -> str:
        SPECIAL_SYMBOLS: dict[str, str] = {"Celtics": "🍀", "Pacers": "🏎️"}

        team_names = [self.game.visiting_team.team_name, self.game.home_team.team_name]

        for n, team_name in enumerate(team_names):
            if SPECIAL_SYMBOLS.get(team_name):
                team_name = f"{team_name} {SPECIAL_SYMBOLS[team_name]}"
            team_names[n] = team_name

        joined_names = " @ ".join(team_names)

        return joined_names

    def format_date(self) -> str:
        return self.game.eastern_time.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )  # todo fix this from saying UTC in Notion

    def format_network(self) -> str:
        return self.game.watchable_broadcaster.disp

    def fetch_league(self) -> str:
        return "NBA"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.NBA.value


class SoccerAssembler(Assembler):
    def __init__(self, broadcast: GameBroadcast, league_types: LeagueTypes):
        self.broadcast = broadcast
        self.league_types = league_types

    def assemble_matchup(self) -> str:
        teams = sorted(
            self.broadcast.program.teams, key=lambda t: t.isHome, reverse=True
        )
        team_names = [team.name for team in teams]
        return " vs ".join(team_names)

    def format_date(self) -> str:
        utc_unaware = self.broadcast.startTime
        utc_aware = utc_unaware.replace(tzinfo=ZoneInfo("UTC"))
        local_aware = utc_aware.astimezone(ZoneInfo("America/Indianapolis"))

        return local_aware.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.broadcast.station.name

    def fetch_league(self) -> str:
        return self.league_types.find_by_ids(
            self.broadcast.leagueId, self.broadcast.parentLeagueId
        ).name

    def format_sport(self) -> str:
        return ElligibleSportsEnum.SOCCER.value
