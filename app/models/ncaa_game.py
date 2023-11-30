from typing import Callable, Optional, cast
from bs4 import ResultSet, Tag
from pydantic import BaseModel
from datetime import datetime
from dateutil.parser import parse
from constants import NCAA_BASKETBALL_GOODLIST
from shared import beginning_of_today, is_date
from dateutil.tz import tzlocal


def parse_datetime(value: str) -> Optional[datetime]:
    return parse(value).astimezone(tzlocal()) if is_date(value) else None


class NcaaGame(BaseModel):
    away_team: str
    home_team: str
    start_time: Optional[datetime]  # optional start_time may say "LIVE"
    broadcasters: list[Optional[str]]

    def watchable_broadcasts(self) -> list[str]:
        return [
            broadcast
            for broadcast in self.broadcasters
            if broadcast in NCAA_BASKETBALL_GOODLIST
        ]


class NcaaResponse(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    elements_container: Tag
    events: list[NcaaGame] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.events = self.convert_events()

    def format_broadcaster(self, col: Tag) -> Optional[list[str]]:
        broadcaster_imgs = col.find_all("img", alt=True)

        broadcaster_text = col.text

        if broadcaster_imgs:
            return [cast(str, img["alt"]) for img in cast(list[Tag], broadcaster_imgs)]

        elif broadcaster_text:
            return broadcaster_text.split("|")

        return []

    def convert_events(self) -> list[NcaaGame]:
        events: list[NcaaGame] = []
        table_body = self.elements_container.find("tbody")

        if isinstance(table_body, Tag):
            rows = table_body.find_all("tr")

            for row in rows:
                cols: ResultSet = row.find_all("td")

                broadcasters = self.format_broadcaster(cols[3])

                events.append(
                    NcaaGame(
                        away_team=cols[0].text,
                        home_team=cols[1].find("span", class_="Table__Team").text,
                        start_time=parse_datetime(cols[2].text),
                        broadcasters=broadcasters,
                    )
                )

        return events

    @property
    def usable_events(self) -> list[NcaaGame]:
        def has_good_broadcasters(event: NcaaGame) -> bool:
            if not event.broadcasters:
                return False
            return not not list(
                set(event.broadcasters).intersection(NCAA_BASKETBALL_GOODLIST)
            )

        return [
            event
            for event in self.events
            if has_good_broadcasters(event)
            and event.start_time
            and event.start_time > beginning_of_today
        ]
