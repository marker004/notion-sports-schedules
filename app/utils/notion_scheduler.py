import asyncio
from typing import Literal, cast

from shared import ElligibleSports, ElligibleSportsEnum, NotionSportsScheduleItem
from shared_items.interfaces.notion import Notion, collect_paginated_api
from shared_items.utils import measure_execution

notion = Notion()
SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"


def filter_existing_notion_games_by_sport(sport: ElligibleSports) -> dict:
    return {
        "property": "Sport",
        "rich_text": {"equals": sport},
    }


def filter_existing_manually_added_notion_games() -> dict:
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

    return filter


def recursively_fetch_existing_notion_games(filter: dict) -> list[dict]:
    return collect_paginated_api(
        notion.client.databases.query, filter=filter, database_id=SCHEDULE_DATABASE_ID
    )


class NotionScheduler:
    def __init__(
        self,
        sport: ElligibleSports,
        fresh_schedule_items: list[NotionSportsScheduleItem],
    ) -> None:
        self.sport: ElligibleSports = sport
        self.fresh_schedule_items = fresh_schedule_items

    @measure_execution(f"scheduling")
    def schedule(self) -> None:
        all_existing_notion_games = self.fetch_existing_games()
        existing_schedule_items = self.assemble_existing_schedule_items(
            all_existing_notion_games
        )

        delete_list, do_nothing_list, add_list = self.group_schedule_items(
            existing_schedule_items, self.fresh_schedule_items
        )
        asyncio.run(self.operate_in_notion(delete_list, do_nothing_list, add_list))

    @measure_execution(f"fetching existing games")
    def fetch_existing_games(self):
        filter = (
            filter_existing_manually_added_notion_games()
            if self.sport == "other"
            else filter_existing_notion_games_by_sport(self.sport)
        )

        return recursively_fetch_existing_notion_games(filter)

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

    async def delete_unuseful_games(self, delete_list: list[NotionSportsScheduleItem]):
        print(f"deleting {len(delete_list)} games")
        # these items should all have notion_ids as they have been fetched from Notion
        await notion.async_delete_all_blocks(
            [cast(str, item.notion_id) for item in delete_list]
        )

    async def insert_new_games(self, insert_list: list[NotionSportsScheduleItem]):
        insert_list_props = self.assemble_insertion_notion_props(insert_list)
        print(f"inserting {len(insert_list)} games")
        await notion.async_add_all_pages(SCHEDULE_DATABASE_ID, insert_list_props)

    async def operate_in_notion(
        self,
        delete_list: list[NotionSportsScheduleItem],
        do_nothing_list: list[NotionSportsScheduleItem],
        add_list: list[NotionSportsScheduleItem],
    ):
        await self.delete_unuseful_games(delete_list)
        print(f"keeping {len(do_nothing_list)} games\n")
        await self.insert_new_games(add_list)
