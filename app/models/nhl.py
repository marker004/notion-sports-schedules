from datetime import datetime
from typing import Literal, Optional, TypedDict
from pydantic import BaseModel, validator

from constants import NHL_BROADCAST_BADLIST, NO_HULU_BADLIST


def normalize_dates(raw_date_string: str) -> datetime:
    unix_timestamp = (
        int(raw_date_string.removeprefix("/Date(").removesuffix(")/")) / 1000
    )
    return datetime.utcfromtimestamp(unix_timestamp)


# class RequestMetadata(TypedDict):
#     timeStamp: datetime

# class Status(TypedDict):
#     abstractGameState: str
#     codedGameState: int
#     detailedState: str
#     statusCode: int
#     startTimeTBD: bool


class Record(BaseModel):
    wins: int
    losses: int
    ot: Optional[int]
    type: str  # Literal if I care


class TeamId(BaseModel):
    id: int
    name: str
    link: str  # url if I care


class Team(BaseModel):
    leagueRecord: Record
    score: int
    team: TeamId


class Teams(BaseModel):
    away: Team
    home: Team


# class Venue(TypedDict):
#     name: str
#     link: str # url if I care


class Broadcast(BaseModel):
    id: int
    name: str
    type: Literal["national", "home", "away"]
    site: Literal["nhl", "nhlCA"]
    language: Literal["en", "fr"]

    def watchable(self) -> bool:
        return self.name not in (NHL_BROADCAST_BADLIST + NO_HULU_BADLIST)


# class Content(TypedDict):
#     link: str # url if I care


class Game(BaseModel):
    # gamePk: int
    # link: str
    # gameType: str
    # season: str
    gameDate: datetime
    # status: Status
    teams: Teams
    # venue: Venue
    broadcasts: list[Broadcast] = []
    # content: Content

    def watchable_broadcasts(self) -> list[Broadcast]:
        return [broadcast for broadcast in self.broadcasts if broadcast.watchable()]

    def any_watchable_broadcasts(self) -> bool:
        return any(self.watchable_broadcasts())


class Date(BaseModel):
    date: datetime
    games: list[Game]
    # totalItems: int
    # totalEvents: int
    # totalGames: int
    # totalMatches: int
    # events: list[dict]
    # matches: list[dict]

    @validator("date", pre=True)
    def normalize_dates(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")
        return value


class LeagueBroadcastSchedule(BaseModel):
    dates: list[Date]
    # copyright: str
    # totalItems: int
    # totalEvents: int
    # totalGames: int
    # totalMatches: int
    # metaData: RequestMetadata
    # wait: int

    def watchable_games(self) -> list[Game]:
        # if not self.broadcasts:
        return [
            game
            for date in self.dates
            for game in date.games
            if game.any_watchable_broadcasts()
        ]

    def usable_events(self) -> list[Game]:
        return self.watchable_games()
        # sorted = self.sorted_broadcasts(watchable)
        # return self.unique_broadcasts_by_match_id(sorted)
