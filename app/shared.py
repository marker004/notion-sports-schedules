from __future__ import annotations
from datetime import datetime, time
from enum import Enum
from typing import Literal, NamedTuple, Optional, TypedDict
from pydantic.dataclasses import dataclass
from shared_items.interfaces import Prop as NotionProp
from shared_items.interfaces.notion import Notion
from shared_items.utils import measure_execution
from dateutil.parser import parser
from dateutil.tz import tzlocal


SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"

notion = Notion()

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


def fetch_all_existing_notion_games_by_sport(sport: ElligibleSports) -> list[dict]:
    game_fetcher = fetch_games_by_sport(sport)

    all_games: list[dict] = []
    next_cursor: Optional[str] = None

    while True:
        response = game_fetcher(next_cursor)
        next_cursor = response["next_cursor"]
        all_games += response["results"]
        if not response["has_more"]:
            break

    return all_games


def fetch_all_existing_manually_added_notion_games() -> list[dict]:
    game_fetcher = fetch_manually_added_games()

    all_games: list[dict] = []
    next_cursor: Optional[str] = None

    while True:
        response = game_fetcher(next_cursor)
        next_cursor = response["next_cursor"]
        all_games += response["results"]
        if not response["has_more"]:
            break

    return all_games


def fetch_games_by_sport(sport: Optional[ElligibleSports] = None):
    def func(start_cursor: Optional[str] = None):
        filter = {
            "property": "Sport",
            "rich_text": {"equals": sport},
        }
        return notion.client.databases.query(
            database_id=SCHEDULE_DATABASE_ID, filter=filter, start_cursor=start_cursor
        )

    return func


def fetch_manually_added_games():
    def func(start_cursor: Optional[str] = None):
        filter: dict[Literal["and"], list[dict]] = {"and": []}

        elligible_sports = [
            sport.value for sport in ElligibleSportsEnum.__members__.values()
        ]

        for sport in elligible_sports:
            filter_section = {
                "property": "Sport",
                "rich_text": {"does_not_equal": sport},
            }
            filter["and"].append(filter_section)

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


def delete_db_items_for_sport(sport: ElligibleSports):
    fetch_games = fetch_games_by_sport(sport)
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
    favorite: str
    notion_id: Optional[str] = None

    @classmethod
    def from_notion_interface(self, notion_row: dict) -> NotionSportsScheduleItem:
        properties = notion_row["properties"]
        converted_date = parser().parse(properties["Date"]["date"]["start"])

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


class NotionScheduler:
    def __init__(
        self,
        sport: ElligibleSports,
        fresh_schedule_items: list[NotionSportsScheduleItem],
    ) -> None:
        self.sport: ElligibleSports = sport
        self.fresh_schedule_items = fresh_schedule_items

    def schedule_them_shits(self) -> None:
        all_existing_notion_games = self.fetch_existing_games()
        existing_schedule_items = self.assemble_existing_schedule_items(
            all_existing_notion_games
        )

        delete_list, do_nothing_list, add_list = self.group_schedule_items(
            existing_schedule_items, self.fresh_schedule_items
        )
        self.operate_in_notion(delete_list, do_nothing_list, add_list)

    @measure_execution(f"fetching existing games")
    def fetch_existing_games(self):
        if self.sport == "other":
            return fetch_all_existing_manually_added_notion_games()
        return fetch_all_existing_notion_games_by_sport(self.sport)

    def assemble_existing_schedule_items(self, notion_rows: list[dict]):
        return [
            NotionSportsScheduleItem.from_notion_interface(notion_game)
            for notion_game in notion_rows
        ]

    def assemble_insertion_notion_props(
        self, insertion_list: list[NotionSportsScheduleItem]
    ):
        return [
            notion.assemble_props(schedule_item.format_for_notion_interface())
            for schedule_item in insertion_list
        ]

    def group_schedule_items(
        self,
        existing_items: list[NotionSportsScheduleItem],
        fresh_items: list[NotionSportsScheduleItem],
    ) -> tuple[
        list[NotionSportsScheduleItem],
        list[NotionSportsScheduleItem],
        list[NotionSportsScheduleItem],
    ]:
        delete_list = list(set(existing_items) - set(fresh_items))
        do_nothing_list = list(set(fresh_items) & set(existing_items))
        add_list = list(set(fresh_items) - set(existing_items))

        return (delete_list, do_nothing_list, add_list)

    @measure_execution("deleting existing games")
    def delete_unuseful_games(self, delete_list: list[NotionSportsScheduleItem]):
        for item in delete_list:
            if item.notion_id:  # should always be true
                notion.client.blocks.delete(block_id=item.notion_id)
        print(f"deleted {len(delete_list)} games")

    @measure_execution("inserting fresh games")
    def insert_new_games(self, insert_list: list[NotionSportsScheduleItem]):
        insert_list_props = self.assemble_insertion_notion_props(insert_list)
        insert_to_database(insert_list_props)
        print(f"inserted {len(insert_list)} games")

    def operate_in_notion(
        self,
        delete_list: list[NotionSportsScheduleItem],
        do_nothing_list: list[NotionSportsScheduleItem],
        add_list: list[NotionSportsScheduleItem],
    ):
        self.delete_unuseful_games(delete_list)
        print(f"keeping {len(do_nothing_list)} games\n")
        self.insert_new_games(add_list)


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

    print(set(flat_list))
