from datetime import datetime
from typing import Literal, TypedDict
from pydantic import BaseModel, Field


# class RequestMetadata(TypedDict):
#     timeStamp: datetime

class Status(TypedDict):
    abstractGameState: str
    codedGameState: int
    detailedState: str
    statusCode: int
    startTimeTBD: bool


class Record(BaseModel):
    wins: int
    losses: int
    ot: int
    type: str # Literal if I care


class TeamId(BaseModel):
    id: int
    name: str
    link: str # url if I care


class Team(BaseModel):
    leagueRecord: Record
    score: int
    team: TeamId


class Teams(TypedDict):
    away: Team
    home: Team


class Venue(TypedDict):
    name: str
    link: str # url if I care

class Broadcast(BaseModel):
    id: int
    name: str
    type: Literal["national", "home", "away"]
    site: Literal["nhl"]
    language: Literal["en"]

class Content(TypedDict):
    link: str # url if I care

class Game(BaseModel):
    gamePk: int
    link: str # todo if I care: type this to url
    gameType: str # todo if I care: type this to Literal
    season: str
    gameDate: datetime
    status: Status
    teams: Teams
    venue: Venue
    broadcasts: list[Broadcast]
    content: Content

class Date(BaseModel):
    date: datetime
    totalItems: int
    totalEvents: int
    totalGames: int
    totalMatches: int
    games: list[Game]
    events: list[dict]
    matches: list[dict]

class LeagueBroadcastSchedule(BaseModel):
    # copyright: str
    # totalItems: int
    # totalEvents: int
    # totalGames: int
    # totalMatches: int
    # metaData: RequestMetadata
    # wait: int
    dates: list[Date]

