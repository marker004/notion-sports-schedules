from typing import Callable
from zoneinfo import ZoneInfo
from constants import (
    MLB_FAVORITE_CRITERIA,
    NATIONAL_FLAGS,
    NBA_FAVORITE_CRITERIA,
    NCAA_TOURNAMENT_FAVORITE_CRITERIA,
    NHL_FAVORITE_CRITERIA,
    SOCCER_FAVORITE_CRITERIA,
)
from models.f1 import F1Race
from models.indycar import IndycarRace
from models.ncaa_bball import Game as NcaaGame
from models.notion_game import NotionGame
from models.soccer import AppleTVFreeSoccer, GameBroadcast, LeagueTypes
from models.mlb import Game as MlbGame, MlbEspnPlusInfo
from models.nba import Game as NbaGame, HboMaxGame
from models.nhl import Game as NhlGame
from models.nhl_espn import Event as NhlEspnPlusGame
from shared import ElligibleSportsEnum, FavoriteCriterion, NotionSportsScheduleItem


class Assembler:
    def __init__(self) -> None:
        self.favorite_criteria: list[FavoriteCriterion] = []

    def format_matchup(self) -> str:
        raise NotImplementedError

    def format_date(self) -> str:
        raise NotImplementedError

    def format_network(self) -> str:
        raise NotImplementedError

    def format_league(self) -> str:
        raise NotImplementedError

    def format_sport(self) -> str:
        raise NotImplementedError

    def format_favorite(self) -> str:
        is_favorite: bool = False
        for criterion in self.favorite_criteria:
            property = criterion["property"]
            comparison = criterion["comparison"]
            value = criterion["value"]
            func: Callable[[], str] = getattr(self, f"format_{property}")
            if comparison == "equals":
                is_favorite = func() == value
            elif comparison == "contains":
                is_favorite = value in func()
            if is_favorite:
                break

        return "Favorite" if is_favorite else "Other"

    def notion_sports_schedule_item(self) -> NotionSportsScheduleItem:
        return NotionSportsScheduleItem(
            matchup=self.format_matchup(),
            date=self.format_date(),
            network=self.format_network(),
            league=self.format_league(),
            sport=self.format_sport(),
            favorite=self.format_favorite(),
        )


class ManualAssembler(Assembler):
    def __init__(self, game: NotionGame):
        self.game = game

    def format_matchup(self) -> str:
        return self.game.matchup

    def format_date(self) -> str:
        return self.game.date

    def format_network(self) -> str:
        return self.game.network

    def format_league(self) -> str:
        return self.game.league

    def format_sport(self) -> str:
        return self.game.sport

    def format_favorite(self) -> str:
        return "Favorite"


class NcaaTournamentAssembler(Assembler):
    def __init__(self, game: NcaaGame):
        self.game = game
        self.favorite_criteria = NCAA_TOURNAMENT_FAVORITE_CRITERIA

    def format_matchup(self) -> str:
        home_team = self.game.team_collection.home_team()
        away_team = self.game.team_collection.away_team()
        if home_team and away_team:
            return f"{away_team.nameShort} ({away_team.seed}) vs {home_team.nameShort} ({home_team.seed}) [{self.game.round.label}]"
        elif home_team:
            return f"TBD vs {home_team.nameShort} ({home_team.seed}) [{self.game.round.label}]"
        elif away_team:
            return f"{away_team.nameShort} ({away_team.seed}) vs TBD [{self.game.round.label}]"
        else:
            return ""

    def format_date(self) -> str:
        return self.game.start_time.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.game.broadcaster.name if self.game.broadcaster else ""

    def format_league(self) -> str:
        return "NCAA Tournament"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.BASKETBALL.value


class NbaBaseAssembler(Assembler):
    def __init__(self) -> None:
        self.favorite_criteria = NBA_FAVORITE_CRITERIA

    def format_league(self) -> str:
        return "NBA"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.NBA.value


class NbaAssembler(NbaBaseAssembler):
    def __init__(self, game: NbaGame):
        super().__init__()
        self.game = game

    def format_matchup(self) -> str:
        team_names = [self.game.visiting_team.team_name, self.game.home_team.team_name]

        return " vs ".join(team_names)

    def format_date(self) -> str:
        return (
            self.game.start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            if self.game.start_datetime
            else ""
        )

    def format_network(self) -> str:
        return self.game.watchable_broadcaster.disp


class HboMaxGameAssembler(NbaBaseAssembler):
    def __init__(self, game: HboMaxGame):
        super().__init__()
        self.game = game

    def format_matchup(self) -> str:
        return self.game.matchup

    def format_date(self) -> str:
        return self.game.datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return f"{self.game.network} (HBO Max)"


class SoccerAssembler(Assembler):
    def __init__(self, broadcast: GameBroadcast, league_types: LeagueTypes):
        self.broadcast = broadcast
        self.league_types = league_types
        self.favorite_criteria = SOCCER_FAVORITE_CRITERIA

    def format_matchup(self) -> str:
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

    def format_league(self) -> str:
        return self.league_types.find_by_ids(
            self.broadcast.leagueId, self.broadcast.parentLeagueId
        ).name

    def format_sport(self) -> str:
        return ElligibleSportsEnum.SOCCER.value


class AppleTVFreeGamesSoccerAssembler(Assembler):
    def __init__(self, game: AppleTVFreeSoccer) -> None:
        super().__init__()
        self.game = game
        self.favorite_criteria = SOCCER_FAVORITE_CRITERIA

    def format_matchup(self) -> str:
        return self.game.matchup

    def format_date(self) -> str:
        return self.game.date.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return "Apple TV+"

    def format_league(self) -> str:
        return f'MLS {NATIONAL_FLAGS["United States"]}'

    def format_sport(self) -> str:
        return ElligibleSportsEnum.SOCCER.value


class NhlBaseAssembler(Assembler):
    def __init__(self) -> None:
        self.favorite_criteria = NHL_FAVORITE_CRITERIA

    def format_league(self) -> str:
        return "NHL"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.NHL.value


class NhlAssembler(NhlBaseAssembler):
    def __init__(self, game: NhlGame):
        super().__init__()
        self.game = game

    def format_matchup(self) -> str:
        home_team = self.game.homeTeam.abbrev
        away_team = self.game.awayTeam.abbrev

        return f"{away_team} vs {home_team}"

    def format_date(self) -> str:
        utc_time = self.game.startTimeUTC
        local_time = utc_time.astimezone(ZoneInfo("America/Indianapolis"))

        return local_time.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        broadcasts = [
            broadcast.network for broadcast in self.game.watchable_broadcasts()
        ]
        return ", ".join(broadcasts)


class NhlEspnPlusAssembler(NhlBaseAssembler):
    def __init__(self, game: NhlEspnPlusGame):
        super().__init__()
        self.game = game

    def format_matchup(self) -> str:
        return self.game.name.replace(" at ", " vs ")

    def format_date(self) -> str:
        utc_time = self.game.date
        local_time = utc_time.astimezone(ZoneInfo("America/Indianapolis"))

        return local_time.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.game.broadcast if self.game.broadcast else ""


class MlbAssembler(Assembler):
    def __init__(self, game: MlbGame):
        self.game = game
        self.favorite_criteria = MLB_FAVORITE_CRITERIA

    def format_matchup(self) -> str:
        home_team = self.game.teams.home.team.name
        away_team = self.game.teams.away.team.name

        return f"{away_team} vs {home_team}"

    def format_date(self) -> str:
        return self.game.gameDate.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return ", ".join(self.game.watchable_broadcasts)

    def format_league(self) -> str:
        if self.game.gameType != "R":
            return f"MLB - {self.game.seriesDescription}"
        return "MLB"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.MLB.value


class MlbEspnPlusAssembler(Assembler):
    def __init__(self, game: MlbEspnPlusInfo):
        self.game = game
        self.favorite_criteria = MLB_FAVORITE_CRITERIA

    def format_matchup(self) -> str:
        return self.game.matchup

    def format_date(self) -> str:
        return self.game.time.strftime("%Y-%m-%dT%H:%M:%S") if self.game.time else ""

    def format_network(self) -> str:
        return "ESPN+"

    def format_league(self) -> str:
        return "MLB"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.MLB.value


class IndycarAssembler(Assembler):
    def __init__(self, race: IndycarRace):
        super().__init__()
        self.race = race

    def format_matchup(self) -> str:
        return self.race.race_name

    def format_date(self) -> str:
        return self.race.start_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def format_network(self) -> str:
        return self.race.channel

    def format_league(self) -> str:
        return "IndyCar"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.INDY_CAR.value


class F1Assembler(Assembler):
    def __init__(self, race: F1Race):
        super().__init__()
        self.race = race

    def format_matchup(self) -> str:
        return self.race.race_name

    def format_date(self) -> str:
        return (
            self.race.start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            if self.race.start_datetime
            else ""
        )

    def format_network(self) -> str:
        return self.race.channel if self.race.channel else ""

    def format_league(self) -> str:
        return "Formula 1"

    def format_sport(self) -> str:
        return ElligibleSportsEnum.F1.value
