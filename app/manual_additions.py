from shared import NotionSportsScheduleItem
from models.notion_game import NotionGame, NotionGames
from utils import (
    NotionScheduler,
    filter_existing_manually_added_notion_games,
    recursively_fetch_existing_notion_games,
)
from utils.assemblers import ManualAssembler


def fetch_games() -> list[dict]:
    filter = filter_existing_manually_added_notion_games()
    return recursively_fetch_existing_notion_games(filter)


def assemble_usable_events(games: list[dict]) -> list[NotionGame]:
    notion_games = NotionGames(
        games=[
            NotionGame.parse_obj({**game["properties"], "notion_id": game["id"]})
            for game in games
        ]
    )

    return notion_games.usable_events()


def assemble_notion_items(games: list[NotionGame]) -> list[NotionSportsScheduleItem]:
    return [ManualAssembler(game).notion_sports_schedule_item() for game in games]


games = fetch_games()
usable_events = assemble_usable_events(games)
fresh_items = assemble_notion_items(usable_events)

NotionScheduler("other", fresh_items).schedule()
