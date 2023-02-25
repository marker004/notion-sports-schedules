from datetime import datetime, time
from enum import Enum
from typing import Literal, Optional
from pydantic.dataclasses import dataclass
from shared_items.interfaces import Prop as NotionProp
from shared_items.interfaces.notion import Notion

SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"

notion = Notion()

beginning_of_today = datetime.combine(datetime.now(), time())

ElligibleSports = Literal["🏀", "⚽"]


class ElligibleSportsEnum(Enum):
    NBA = "🏀"
    SOCCER = "⚽"


def fetch_all_games_by_sport(sport: ElligibleSports):
    def func(next_cursor=None):
        filter = {
            "property": "Sport",
            "rich_text": {"equals": sport},
        }
        return notion.client.databases.query(
            database_id=SCHEDULE_DATABASE_ID, filter=filter, next_cursor=next_cursor
        )

    return func


def fetch_only_future_games_by_sport(sport: ElligibleSports):
    def func(next_cursor: Optional[str] = None):
        filter = {
            "and": [
                {
                    "property": "Date",
                    "date": {
                        "on_or_after": beginning_of_today.strftime("%Y-%m-%dT%H:%M:%S")
                    },
                },
                {
                    "property": "Sport",
                    "rich_text": {"equals": sport},
                },
            ]
        }
        return notion.client.databases.query(
            database_id=SCHEDULE_DATABASE_ID, filter=filter, next_cursor=next_cursor
        )

    return func


@dataclass
class NotionSportsScheduleItem:
    matchup: str
    date: str
    network: str
    league: str
    sport: str

    def format_for_notion_interface(self) -> list[NotionProp]:
        return [
            {
                "name": "Matchup",
                "type": "title",
                "content": self.matchup,
            },
            {"name": "Date", "type": "date", "content": self.date},
            {
                "name": "Network",
                "type": "rich_text",
                "content": self.network,
            },
            {
                "name": "League",
                "type": "rich_text",
                "content": self.league,
            },
            {"name": "Sport", "type": "rich_text", "content": self.sport},
        ]
