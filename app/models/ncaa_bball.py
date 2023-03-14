from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, validator


class Broadcaster(BaseModel):
    name: str


class Round(BaseModel):
    label: str
    roundNumber: int
    subtitle: str
    title: str


class Team(BaseModel):
    isHome: bool
    nameShort: str
    seed: int


class Teams(BaseModel):
    teams: list[Team]

    def home_team(self) -> Optional[Team]:
        return next((team for team in self.teams if team.isHome), None)

    def away_team(self) -> Optional[Team]:
        return next((team for team in self.teams if not team.isHome), None)


class Game(BaseModel):
    class Config:
        allow_population_by_field_name = True

    start_time: datetime = Field(alias="startTimeEpoch")
    round: Round
    broadcaster: Optional[Broadcaster]
    team_collection: Teams = Field(alias="teams")

    @validator("start_time")
    def convert_start_time_to_local(cls, value):
        if isinstance(value, datetime):
            return value.astimezone(ZoneInfo("America/Indianapolis"))

    @validator("team_collection", pre=True)
    def convert_list_of_teams(cls, value):
        if isinstance(value, list):
            return Teams(teams=value)


class GameCollection(BaseModel):
    games: list[Game]

    def usable_games(self) -> list[Game]:
        return [
            game
            for game in self.games
            if game.team_collection.teams
            and game.broadcaster
            and game.start_time.replace(tzinfo=None) > datetime.now()
        ]
