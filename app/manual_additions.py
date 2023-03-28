from shared import (
    NotionScheduler,
    NotionSportsScheduleItem,
    fetch_all_existing_manually_added_notion_games,
)
from models.notion_game import NotionGame, NotionGames
from utils.assemblers import ManualAssembler

def fetch_games() -> list[dict]:
    return fetch_all_existing_manually_added_notion_games()

def assemble_usable_games(games: list[dict]) -> list[NotionGame]:
    notion_games = NotionGames(
        games=[
            NotionGame.parse_obj({**game["properties"], "notion_id": game["id"]})
            for game in games
        ]
    )

    return notion_games.usable_games()


def assemble_notion_items(games: list[NotionGame]) -> list[NotionSportsScheduleItem]:
    return [ManualAssembler(game).notion_sports_schedule_item() for game in games]

games = fetch_games()
usable_games = assemble_usable_games(games)
fresh_items = assemble_notion_items(usable_games)

NotionScheduler("other", fresh_items).schedule_them_shits()
