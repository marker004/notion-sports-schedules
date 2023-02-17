from datetime import datetime, time
from pydantic.dataclasses import dataclass
from shared_items.interfaces import Prop as NotionProp

SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"


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