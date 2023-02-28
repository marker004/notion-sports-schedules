from datetime import datetime
from typing import Optional, TypedDict
from pydantic import BaseModel, validator
from dataclasses import InitVar
from pydantic.dataclasses import dataclass
from constants import NATIONAL_FLAGS, SOCCER_BROADCAST_BADLIST
from itertools import groupby


def normalize_dates(raw_date_string: str) -> datetime:
    unix_timestamp = (
        int(raw_date_string.removeprefix("/Date(").removesuffix(")/")) / 1000
    )
    return datetime.utcfromtimestamp(unix_timestamp)


class Station(BaseModel):
    name: str
    # callSign: Optional[str]
    # stationId: str
    # affiliateId: Optional[str]
    # affiliateCallSign: Optional[str]
    ## type: Optional[str] # mypy needs 2 comment hashes here, "type" is a reserved word
    # blockedCountryCodes: Optional[list[Union[str, int]]]


class Team(BaseModel):
    name: str
    isHome: bool
    # teamBrandId: str


class Program(BaseModel):
    teams: list[Team]
    # rootId: str


# class Affiliate(BaseModel):
#     langCode: str
#     title: str
#     subtitle: str
#     link: str  # convert to URL if I care
#     callToAction: str
#     imageUrl: str  # convert to URL if I care
#     disclaimer: str


class GameBroadcast(BaseModel):
    startTime: datetime
    station: Station
    matchId: int
    leagueId: int
    parentLeagueId: int
    program: Program
    tags: list[str]
    endTime: Optional[datetime]
    # qualifiers: list[str]
    # stationId: str
    # bet365MatchId: int
    # externalId: Optional[str]
    # affiliates: list[Affiliate]

    @validator("startTime", "endTime", pre=True)
    def normalize_dates(cls, value):
        if isinstance(value, str):
            return normalize_dates(value)
        return value


class GameBroadcastCollection(BaseModel):
    game_broadcasts: list[GameBroadcast]

    @staticmethod
    def watchable_broadcasts(broadcasts: list[GameBroadcast]) -> list[GameBroadcast]:
        return [
            broadcast
            for broadcast in broadcasts
            if broadcast.station.name not in SOCCER_BROADCAST_BADLIST
            and "live" in broadcast.tags
        ]

    @staticmethod
    def sorted_broadcasts(broadcasts: list[GameBroadcast]) -> list[GameBroadcast]:
        return sorted(broadcasts, key=lambda b: b.startTime)

    @staticmethod
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

    # todo: test this
    def usable_games(self) -> list[GameBroadcast]:
        watchable = self.watchable_broadcasts(self.game_broadcasts)
        sorted = self.sorted_broadcasts(watchable)
        return self.unique_broadcasts_by_match_id(sorted)


class League(BaseModel):
    id: int
    name: str


class Matches(BaseModel):
    leagues: list[League]


class LeagueDict(TypedDict):
    id: int
    name: str


class CountryEntity(TypedDict):
    name: str
    leagues: list[LeagueDict]


@dataclass
class LeagueTypes:
    international: InitVar[list[CountryEntity]]
    countries: InitVar[list[CountryEntity]]
    leagues: Optional[list[League]] = None

    def __post_init__(
        self, international: list[CountryEntity], countries: list[CountryEntity]
    ):
        leagues: list[League] = []

        for entity in international:
            for league in entity["leagues"]:
                leagues.append(League(**league))

        for country in countries:
            for league in country["leagues"]:
                if NATIONAL_FLAGS.get(country['name']):
                    league["name"] += f" {NATIONAL_FLAGS.get(country['name'])}"
                else:
                    league["name"] += f" - {country['name']}"

                leagues.append(League(**league))

        self.leagues = leagues

    def find_by_ids(self, id: int, parent_id: int) -> League:
        default = League(id=0, name="")
        if not self.leagues:
            return default
        return next(
            (
                league
                for league in self.leagues
                if league.id == id or league.id == parent_id
            ),
            default,
        )
