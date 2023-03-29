from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, validator

from constants import MLB_BROADCAST_BADLIST


class TeamId(BaseModel):
    id: int
    name: str
    link: str


class Team(BaseModel):
    # isContextTeam: bool
    # isFollowed: bool
    # isFavorite: bool
    # leagueRecord: dict
    team: TeamId
    # splitSquad: bool
    # seriesNumber: Optional[int]


class Teams(BaseModel):
    home: Team
    away: Team


class VideoResolution(BaseModel):
    code: str
    resolutionShort: str
    resolutionFull: str


class Broadcast(BaseModel):
    id: int
    name: str
    type: Literal["TV", "AM", "FM"]
    language: Literal["en", "fr", "es"]
    homeAway: Optional[Literal["home", "away"]]
    isNational: Optional[bool]
    callSign: Optional[str]
    videoResolution: Optional[VideoResolution]


class Game(BaseModel):
    # sortIndex1: int
    # sortIndex2: int
    # sortIndex3: int
    # sortIndex4: int
    # sortIndex5: int
    teams: Teams
    # gamePk: int
    # link: str
    gameType: Literal["S", "R", "E"]
    # season: str
    gameDate: datetime
    officialDate: datetime
    # status: dict
    # venue: dict
    broadcasts: list[Broadcast] = []
    # content: dict
    # gameNumber: int
    # publicFacing: bool
    # doubleHeader: str
    # gamedayType: str
    # tiebreaker: str
    # calendarEventID: str
    # seasonDisplay: str
    # dayNight: str
    # scheduledInnings: int
    # reverseHomeAwayStatus: bool
    # inningBreakLength: int
    # gamesInSeries: Optional[int]
    # seriesGameNumber: Optional[int]
    seriesDescription: Literal["Spring Training", "Regular Season", "Exhibition"]
    # flags: dict
    # recordSource: str
    # ifNecessary: str
    # ifNecessaryDescription: str
    # gameUtils: dict
    # linescore: dict

    @validator("officialDate", pre=True)
    def official_date(cls, value):
        if isinstance(value, str):
            # return parser.parse(value)
            return datetime.strptime(value, "%Y-%m-%d")
        return value

    @property
    def watchable_broadcasts(self) -> list[str]:
        return list(
            set(
                [
                    broadcast.name
                    for broadcast in self.broadcasts
                    if broadcast.name not in MLB_BROADCAST_BADLIST
                ]
            )
        )


class Date(BaseModel):
    date: datetime
    totalItems: int
    totalEvents: int
    totalGames: int
    totalGamesInProgress: int
    games: list[Game]
    events: list[dict]

    @validator("date", pre=True)
    def normalize_dates(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")
        return value


class MlbResponse(BaseModel):
    copyright: str
    totalItems: int
    totalEvents: int
    totalGames: int
    totalGamesInProgress: int
    dates: list[Date]
    headers: dict
    status: int

    def games(self) -> list[Game]:
        return [game for date in self.dates for game in date.games]

    def usable_games(self) -> list[Game]:
        good_games: list[Game] = []
        for game in self.games():
            if any(
                [
                    broadcast
                    for broadcast in game.broadcasts
                    if broadcast.name not in MLB_BROADCAST_BADLIST
                ]
            ):
                good_games.append(game)
        # unique_names = list(set([broadcast.name for game in self.games() for broadcast in game.broadcasts]))
        return good_games
