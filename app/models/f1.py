from datetime import datetime
from typing import Optional, cast
from bs4 import Tag
from pydantic import BaseModel, validator
from dateutil.parser import parse
from constants import F1_CHANNEL_GOODLIST, NO_HULU_BADLIST
from shared import beginning_of_today, is_date
from dateutil.tz import tzlocal


def convert_race_name(element: Tag) -> str:
    title = element.find("a")
    if isinstance(title, Tag):
        return title.text
    else:  # this should never happen
        return element.text


def parse_datetime(value: str) -> Optional[datetime]:
    return parse(value).astimezone(tzlocal()) if is_date(value) else None


class F1Race(BaseModel):
    date_range: str
    race_name: str
    start_datetime: Optional[datetime]
    channel: Optional[str]

    @validator("start_datetime", pre=True)
    def convert_datetime(cls, value):
        return parse_datetime(value)


class F1Response(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    race_elements_container: Tag
    races: list[F1Race] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.races = self.convert_races()

    def convert_races(self) -> list[F1Race]:
        races: list[F1Race] = []
        table_body = self.race_elements_container.find("tbody")

        if isinstance(table_body, Tag):
            rows = table_body.find_all("tr")

            for row in rows:
                cols = cast(list[Tag], row.find_all("td"))

                races.append(
                    F1Race(
                        date_range=cols[0].text,
                        race_name=convert_race_name(cols[1]),
                        start_datetime=cols[2].text,
                        channel=cols[3].text,
                    )
                )

        return races

    @property
    def usable_events(self) -> list[F1Race]:
        return [
            race
            for race in self.races
            if race.channel in list(set(F1_CHANNEL_GOODLIST) - set(NO_HULU_BADLIST))
            and race.start_datetime
            and race.start_datetime > beginning_of_today
        ]
