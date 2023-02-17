from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, validator

def normalize_dates(raw_date_string: str) -> datetime:
    unix_timestamp = (
        int(raw_date_string.removeprefix("/Date(").removesuffix(")/")) / 1000
    )
    return datetime.utcfromtimestamp(unix_timestamp)

class Station(BaseModel):
    callSign: Optional[str]
    stationId: str
    affiliateId: Optional[str]
    affiliateCallSign: Optional[str]
    name: str
    type: Optional[str]
    blockedCountryCodes: Optional[list[Union[str, int]]]


class Team(BaseModel):
    name: str
    isHome: bool
    teamBrandId: str

class Program(BaseModel):
    rootId: str
    teams: list[Team]


class Affiliate(BaseModel):
    langCode: str
    title: str
    subtitle: str
    link: str # convert to URL if I care
    callToAction: str
    imageUrl: str # convert to URL if I care
    disclaimer: str

class GameBroadcast(BaseModel):
    startTime: datetime
    endTime: Optional[datetime]
    qualifiers: list[str]
    station: Station
    stationId: str
    matchId: int
    leagueId: int
    parentLeagueId: int
    program: Program
    bet365MatchId: int
    externalId: Optional[str]
    affiliates: list[Affiliate]
    tags: list[str]

    @validator('startTime', 'endTime', pre=True)
    def normalize_dates(cls, value):
        if isinstance(value, str):
            return normalize_dates(value)
        return value

class League(BaseModel):
    id: int
    name: str

class Matches(BaseModel):
    leagues: list[League]
