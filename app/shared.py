from __future__ import annotations
from datetime import datetime, time
from enum import Enum
from typing import Literal, Optional
from pydantic.dataclasses import dataclass
from shared_items.interfaces import Prop as NotionProp
from shared_items.interfaces.notion import Notion
from dateutil.parser import parser


SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"

notion = Notion()

beginning_of_today = datetime.combine(datetime.now(), time())

ElligibleSports = Literal["🏀", "⚽", "🏒", "⚾", "🏁", "🏎️"]


class ElligibleSportsEnum(Enum):
    NBA = "🏀"
    SOCCER = "⚽"
    NHL = "🏒"
    MLB = "⚾"
    INDY_CAR = "🏁"
    F1 = "🏎️"


def fetch_all_games_by_sport(sport: ElligibleSports):
    def func(start_cursor=None):
        filter = {
            "property": "Sport",
            "rich_text": {"equals": sport},
        }
        return notion.client.databases.query(
            database_id=SCHEDULE_DATABASE_ID, filter=filter, start_cursor=start_cursor
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


def clear_db_for_sport(sport: ElligibleSports):
    fetch_games = fetch_all_games_by_sport(sport)
    delete_games = notion.recursive_fetch_and_delete(fetch_games)
    delete_games()


def insert_to_database(all_props: list[dict]):
    row_creator = notion.create_row_for_database(SCHEDULE_DATABASE_ID)
    for props in all_props:
        row_creator(props)


@dataclass
class NotionSportsScheduleItem:
    matchup: str
    date: str
    network: str
    league: str
    sport: str

    @classmethod
    def from_notion_interface(self, dict) -> NotionSportsScheduleItem:
        converted_date = parser().parse(dict["Date"]["date"]["start"])

        matchup = dict["Matchup"]["title"][0]["plain_text"]
        date = converted_date.strftime("%Y-%m-%dT%H:%M:%S")
        network = dict["Network"]["rich_text"][0]["plain_text"]
        league = dict["League"]["rich_text"][0]["plain_text"]
        sport = dict["Sport"]["rich_text"][0]["plain_text"]

        return NotionSportsScheduleItem(
            matchup=matchup, date=date, network=network, league=league, sport=sport
        )

    def __eq__(self, other) -> bool:
        return sorted(self.__dict__.items()) == sorted(other.__dict__.items())

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

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
        ]
