from datetime import datetime
from typing import cast
from bs4 import Tag
from pydantic import BaseModel, validator
from dateutil.parser import parse
from unidecode import unidecode
from shared import beginning_of_today
from dateutil.tz import tzlocal


from constants import INDYCAR_CHANNEL_GOODLIST


def convert_date(element: Tag) -> str:
    line_break = element.find("br")
    if isinstance(line_break, Tag):
        line_break.replaceWith(" ")
    spaced_text = element.text
    decoded_text = unidecode(spaced_text)
    return decoded_text.replace("Noon", "12:00 PM").replace(" ET", "")


def convert_race_name(element: Tag) -> str:
    title = element.find("b")
    if isinstance(title, Tag):
        return title.text
    else:  # this should never happen
        return element.text


class IndycarRace(BaseModel):
    start_datetime: datetime
    race_name: str
    channel: str

    @validator('start_datetime', pre=True)
    def convert_datetime(cls, value):
        return parse(value).astimezone(tzlocal())


class IndycarResponse(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    race_elements_container: Tag
    races: list[IndycarRace] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.races = self.convert_races()

    def convert_races(self) -> list[IndycarRace]:
        races: list[IndycarRace] = []
        rows = self.race_elements_container.find_all(
            True, {"class": ["oddrow", "evenrow"]}
        )

        for row in rows:
            cols = cast(list[Tag], row.find_all("td"))

            races.append(
                IndycarRace(
                    start_datetime=convert_date(cols[0]),
                    race_name=convert_race_name(cols[1]),
                    channel=cols[2].text,
                )
            )

        return races

    @property
    def usable_races(self) -> list[IndycarRace]:
        return [
            race
            for race in self.races
            if race.channel in INDYCAR_CHANNEL_GOODLIST
            and race.start_datetime > beginning_of_today
        ]
