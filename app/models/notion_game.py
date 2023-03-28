from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

from dateutil.parser import parser


class NotionGame(BaseModel):
    network: str = Field(alias="Network")
    date: str = Field(alias="Date")
    league: str = Field(alias="League")
    favorite: str = Field(alias="Favorite")
    sport: str = Field(alias="Sport")
    matchup: str = Field(alias="Matchup")
    notion_id: Optional[str] = None


    @validator("network", "league", "sport", "favorite", pre=True)
    def convert_rich_text_fields(cls, value: dict):
        return value["rich_text"][0]["plain_text"]

    @validator("matchup", pre=True)
    def convert_title_field(cls, value: dict):
        return value["title"][0]["plain_text"]

    @validator("date", pre=True)
    def convert_date_fields(cls, value: dict):
        converted_date = parser().parse(value["date"]["start"])
        return converted_date.strftime("%Y-%m-%dT%H:%M:%S")


    def is_upcoming(self) -> bool:
        return parser().parse(self.date) > datetime.now()


class NotionGames(BaseModel):
    games: list[NotionGame]

    def usable_games(self) -> list[NotionGame]:
        return [game for game in self.games if game.is_upcoming()]