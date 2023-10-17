from datetime import datetime
from typing import Literal, Optional, Union
from dateutil.parser import parse
from dateutil.tz import tzlocal

from pydantic import BaseModel, Field, validator
from constants import NBA_BROADCASTER_BADLIST, NO_HULU_BADLIST
from shared import beginning_of_today, is_date


class Team(BaseModel):
    team_name: str = Field(alias="tn")
    # tid: int
    # record: str = Field(alias="re")
    # team_abbreviation: str = Field(alias="ta")
    # team_city: str = Field(alias="tc")
    # score: str = Field(alias="s")


class Broadcaster(BaseModel):
    disp: str
    scope: Literal["home", "away", "can", "natl"]
    type: Literal["tv", "radio"]
    # seq: int
    # language: Literal["English"] = Field(alias="lan")
    # url: Optional[str]  # urlparse into ParseResult?

    def watchable(self) -> bool:
        return (
            self.type == "tv"
            and self.scope == "natl"
            and self.disp not in (NBA_BROADCASTER_BADLIST + NO_HULU_BADLIST)
        )


class Broadcast(BaseModel):
    broadcast: list[Broadcaster] = Field(alias="b")


class Game(BaseModel):
    start_datetime: Optional[datetime] = Field(alias="etm")
    broadcasting: Broadcast = Field(alias="bd")
    visiting_team: Team = Field(alias="v")
    home_team: Team = Field(alias="h")
    # gid: str
    # gcode: str
    # series_summary: str = Field(alias="seri")
    # game_date: date = Field(alias="gdte")
    # arena: str = Field(alias="an")
    # city: str = Field(alias="ac")
    # state: str = Field(alias="as")
    # game_status: str = Field(alias="stt")
    # game_date_utc: date = Field(alias="gdtutc")
    # game_time_utc: time = Field(alias="utctm")

    @validator("start_datetime", pre=True)
    def convert_datetime(cls, value):
        return parse(value).astimezone(tzlocal()) if is_date(value) else None

    def watchable(self) -> bool:
        return any(
            [broadcaster.watchable() for broadcaster in self.broadcasting.broadcast]
        )

    @property
    def watchable_broadcaster(self) -> Broadcaster:
        return [
            broadcaster
            for broadcaster in self.broadcasting.broadcast
            if broadcaster.watchable()
        ][0]


class MonthSchedule(BaseModel):
    month: str = Field(alias="mon")
    games: list[Game] = Field(alias="g")


class LeagueSchedule(BaseModel):
    month_schedule: list[MonthSchedule] = Field(alias="mscd")

    def usable_events(self) -> list[Game]:
        return [
            game
            for month in self.month_schedule
            for game in month.games
            if game.start_datetime
            and game.start_datetime > beginning_of_today
            and game.watchable()
        ]

    class Config:
        allow_population_by_field_name = True
