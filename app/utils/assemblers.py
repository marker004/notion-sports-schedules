from zoneinfo import ZoneInfo
from models.f1 import F1Race
from models.indycar import IndycarRace
from models.soccer import GameBroadcast, LeagueTypes
from models.mlb import Game as MlbGame
from models.nba import Game as NbaGame
from models.nhl import Game as NhlGame
from models.nhl_espn import Event as NhlEspnPlusGame
from shared import ElligibleSportsEnum, NotionSportsScheduleItem


class Assembler:
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
        return self.game.eastern_time.strftime("%Y-%m-%dT%H:%M:%S")

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


class NhlBaseAssembler(Assembler):
    def fetch_league(self) -> str:
        return "NHL"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.NHL.value


class NhlAssembler(NhlBaseAssembler):
    def __init__(self, game: NhlGame):
        self.game = game

    def assemble_matchup(self) -> str:
        home_team = self.game.teams.home.team.name
        away_team = self.game.teams.away.team.name

        return f"{away_team} vs {home_team}"

    def format_date(self) -> str:
        utc_time = self.game.gameDate
        local_time = utc_time.astimezone(ZoneInfo("America/Indianapolis"))

        return local_time.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        broadcasts = [broadcast.name for broadcast in self.game.watchable_broadcasts()]
        return ", ".join(broadcasts)


class NhlEspnPlusAssembler(NhlBaseAssembler):
    def __init__(self, game: NhlEspnPlusGame):
        self.game = game

    def assemble_matchup(self) -> str:
        return self.game.name.replace(" at ", " vs ")

    def format_date(self) -> str:
        utc_time = self.game.date
        local_time = utc_time.astimezone(ZoneInfo("America/Indianapolis"))

        return local_time.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.game.broadcast


class MlbAssembler(Assembler):
    def __init__(self, game: MlbGame):
        self.game = game

    def assemble_matchup(self) -> str:
        home_team = self.game.teams.home.team.name
        away_team = self.game.teams.away.team.name

        return f"{away_team} vs {home_team}"

    def format_date(self) -> str:
        # todo: UTC problem
        return self.game.gameDate.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return ", ".join(self.game.watchable_broadcasts)

    def fetch_league(self) -> str:
        if self.game.gameType != "R":
            return f"MLB - {self.game.seriesDescription}"
        return "MLB"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.MLB.value

class IndycarAssembler(Assembler):
    def __init__(self, race: IndycarRace):
        self.race = race

    def assemble_matchup(self) -> str:
        return self.race.race_name

    def format_date(self) -> str:
        # todo: UTC problem
        return self.race.race_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        utc_unaware = self.race.race_datetime
        utc_aware = utc_unaware.replace(tzinfo=ZoneInfo("UTC"))
        local_aware = utc_aware.astimezone(ZoneInfo("America/Indianapolis"))

        return local_aware.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.race.channel

    def fetch_league(self) -> str:
        return "IndyCar"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.INDY_CAR.value

class F1Assembler(Assembler):
    def __init__(self, race: F1Race):
        self.race = race

    def assemble_matchup(self) -> str:
        return self.race.race_name

    def format_date(self) -> str:
        # todo: UTC problem
        return self.race.race_datetime.strftime("%Y-%m-%dT%H:%M:%S") if self.race.race_datetime else ''
        utc_unaware = self.race.race_datetime
        utc_aware = utc_unaware.replace(tzinfo=ZoneInfo("UTC"))
        local_aware = utc_aware.astimezone(ZoneInfo("America/Indianapolis"))

        return local_aware.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.race.channel if self.race.channel else ''

    def fetch_league(self) -> str:
        return "Formula 1"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.F1.value
