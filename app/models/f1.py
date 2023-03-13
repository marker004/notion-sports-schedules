from datetime import datetime
from typing import Optional, cast
from bs4 import Tag
from pydantic import BaseModel
from dateutil.parser import parse
from constants import F1_CHANNEL_GOODLIST
from shared import beginning_of_today


def is_date(possible_date: str) -> bool:
    try:
        parse(possible_date, fuzzy=True)
        return True

    except ValueError:
        return False


def convert_race_name(element: Tag) -> str:
    title = element.find("a")
    if isinstance(title, Tag):
        return title.text
    else:  # this should never happen
        return element.text


class F1Race(BaseModel):
    date_range: str
    race_name: str
    winner_lights_out: str
    channel: Optional[str]

    @property
    def race_datetime(self) -> Optional[datetime]:
        return (
            parse(self.winner_lights_out) if is_date(self.winner_lights_out) else None
        )


class F1Response(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    race_elements_container: Tag

    @property
    def races(self) -> list[F1Race]:
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
                        winner_lights_out=cols[2].text,
                        channel=cols[3].text,
                    )
                )

        return races

    @property
    def usable_races(self) -> list[F1Race]:
        return [
            race
            for race in self.races
            if race.channel in F1_CHANNEL_GOODLIST
            and race.race_datetime
            and race.race_datetime > beginning_of_today
        ]
