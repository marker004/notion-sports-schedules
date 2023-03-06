from datetime import datetime
from typing import cast
from bs4 import Tag
from pydantic import BaseModel
from dateutil.parser import parse
from unidecode import unidecode
from shared import beginning_of_today


from constants import INDYCAR_CHANNEL_GOODLIST


def convert_date(element: Tag) -> str:
    line_break = element.find("br")
    if isinstance(line_break, Tag):
        line_break.replaceWith(" ")
    spaced_text = element.text
    decoded_text = unidecode(spaced_text)
    return decoded_text.replace("Noon ET", "12:00 PM")

def convert_race_name(element: Tag) -> str:
    title = element.find('b')
    if isinstance(title, Tag):
        return title.text
    else: #this should never happen
        return element.text


class IndycarRace(BaseModel):
    date: str
    race_name: str
    channel: str

    @property
    def race_datetime(self) -> datetime:
        return parse(self.date)


class IndycarResponse(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    race_elements_container: Tag

    @property
    def races(self) -> list[IndycarRace]:
        races: list[IndycarRace] = []
        rows = self.race_elements_container.find_all(
            True, {"class": ["oddrow", "evenrow"]}
        )

        for row in rows:
            cols = cast(list[Tag], row.find_all("td"))

            races.append(
                IndycarRace(
                    date=convert_date(cols[0]),
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
            and race.race_datetime > beginning_of_today
        ]
