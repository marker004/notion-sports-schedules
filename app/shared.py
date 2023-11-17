from __future__ import annotations
from datetime import datetime, time
from enum import Enum
from typing import Literal, NamedTuple, Optional, TypedDict
from pydantic.dataclasses import dataclass
from shared_items.interfaces import Prop as NotionProp
from dateutil.parser import parse
from dateutil.tz import tzlocal

TAB = "\t"

SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"

beginning_of_today = datetime.combine(datetime.now(), time()).astimezone(tzlocal())

ElligibleSports = Literal["🏀", "⚽", "🏒", "⚾", "🏁", "🏎️", "⛹️", "other"]


class ElligibleSportsEnum(Enum):
    NBA = "🏀"
    SOCCER = "⚽"
    NHL = "🏒"
    MLB = "⚾"
    INDY_CAR = "🏁"
    F1 = "🏎️"
    BASKETBALL = "⛹️"


@dataclass
class NotionSportsScheduleItem:
    matchup: str
    date: str
    network: str
    league: str
    sport: str
    favorite: str
    notion_id: Optional[str] = None

    @classmethod
    def from_notion_interface(self, notion_row: dict) -> NotionSportsScheduleItem:
        properties = notion_row["properties"]
        converted_date = parse(properties["Date"]["date"]["start"])

        matchup = properties["Matchup"]["title"][0]["plain_text"]
        date = converted_date.strftime("%Y-%m-%dT%H:%M:%S")
        network = properties["Network"]["rich_text"][0]["plain_text"]
        league = properties["League"]["rich_text"][0]["plain_text"]
        sport = properties["Sport"]["rich_text"][0]["plain_text"]
        favorite = (
            properties["Favorite"]["rich_text"][0]["plain_text"]
            if len(properties["Favorite"]["rich_text"])
            else ""
        )

        notion_id = notion_row["id"]

        return NotionSportsScheduleItem(
            matchup=matchup,
            date=date,
            network=network,
            league=league,
            sport=sport,
            favorite=favorite,
            notion_id=notion_id,
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, NotionSportsScheduleItem):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __hash__(self):
        dicted = {**self.__dict__}
        dicted.pop("notion_id", None)
        return hash(tuple(sorted(dicted.items())))

    def format_for_notion_interface(self) -> list[NotionProp]:
        return [
            {
                "name": "Matchup",
                "type": "title",
                "content": {
                    "content": self.matchup,
                },
            },
            {
                "name": "Date",
                "type": "date",
                "content": {
                    "start": self.date,
                    "time_zone": "America/Indianapolis",
                },
            },
            {
                "name": "Network",
                "type": "rich_text",
                "content": {
                    "content": self.network,
                },
            },
            {
                "name": "League",
                "type": "rich_text",
                "content": {
                    "content": self.league,
                },
            },
            {"name": "Sport", "type": "rich_text", "content": {"content": self.sport}},
            {
                "name": "Favorite",
                "type": "rich_text",
                "content": {"content": self.favorite},
            },
        ]


class FavoriteCriterion(TypedDict):
    property: Literal["sport", "league", "matchup"]
    comparison: Literal["equals", "contains"]
    value: str


class AppleTVGameInfo(NamedTuple):
    relative_date: str
    matchup: str
    league: str


def log_good_networks(items: list[NotionSportsScheduleItem]) -> None:
    all_good_networks: list[str] = []
    for item in items:
        all_good_networks.append(item.network)

    flat_list = [item for sublist in all_good_networks for item in sublist.split(", ")]

    print(f"{TAB}Good networks: {', '.join(set(flat_list))}")


def is_date(possible_date: str) -> bool:
    try:
        parse(possible_date, fuzzy=True)
        return True

    except ValueError:
        return False
