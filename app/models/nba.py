from datetime import date, time, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

BROADCASTER_BADLIST = ["NBA TV"]

class Team(BaseModel):
    tid: int
    record: str = Field(alias="re")
    team_abbreviation: str = Field(alias="ta")
    team_name: str = Field(alias="tn")
    team_city: str = Field(alias="tc")
    score: str = Field(alias="s")


class Broadcaster(BaseModel):
    seq: int
    disp: str
    scope: Literal["home", "away", "can", "natl"]
    type: Literal["tv", "radio"]
    language: Literal["English"] = Field(alias="lan")
    url: Optional[str]  # urlparse into ParseResult?

    def watchable(self) -> bool:
        return (
            self.type == "tv"
            and self.scope == "natl"
            and self.disp not in BROADCASTER_BADLIST
        )


class Broadcast(BaseModel):
    broadcast: list[Broadcaster] = Field(alias="b")


class Game(BaseModel):
    gid: str
    gcode: str
    series_summary: str = Field(alias="seri")
    game_date: date = Field(alias="gdte")
    arena: str = Field(alias="an")
    city: str = Field(alias="ac")
    state: str = Field(alias="as")
    game_status: str = Field(alias="stt")
    eastern_time: datetime = Field(alias="etm")
    broadcasting: Broadcast = Field(alias="bd")
    visiting_team: Team = Field(alias="v")
    home_team: Team = Field(alias="h")
    game_date_utc: date = Field(alias="gdtutc")
    game_time_utc: time = Field(alias="utctm")

    def watchable(self) -> bool:
        return any([broadcaster.watchable() for broadcaster in self.broadcasting.broadcast])

    @property
    def watchable_broadcaster(self) -> Broadcaster:
        return [broadcaster for broadcaster in self.broadcasting.broadcast if broadcaster.watchable()][0]


class MonthSchedule(BaseModel):
    month: str = Field(alias="mon")
    games: list[Game] = Field(alias="g")


class LeagueSchedule(BaseModel):
    month_schedule: list[MonthSchedule] = Field(alias="mscd")

    class Config:
        allow_population_by_field_name = True