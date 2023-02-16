from datetime import date, time, datetime
from pprint import pp
from typing import Any, Literal, Optional, cast
from requests import get, Response
import json

from pydantic import BaseModel, Field
from requests import Response

from shared_items.interfaces.notion import Notion, Prop as NotionProp

# SEASON_DATE_BOOKENDS = ["2022-10-18", "2023-06-18"]

SCHEDULE_DATABASE_ID = "7890f1c1844444228b0016ad68c07d22"

notion = Notion()

# def monthlist(dates: list[date]) -> list[str]:
#     start, end = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
#     total_months = lambda dt: dt.month + 12 * dt.year
#     mlist = []
#     for tot_m in range(total_months(start)-1, total_months(end)):
#         y, m = divmod(tot_m, 12)
#         mlist.append(datetime(y, m+1, 1).strftime("%B"))
#     return mlist

# SEASON_MONTHS = monthlist(SEASON_DATE_BOOKENDS)


class Team(BaseModel):
    tid: int
    record: str = Field(alias="re")
    team_abbreviation: str = Field(alias="ta")
    team_name: str = Field(alias="tn")
    team_city: str = Field(alias="tc")
    score: str = Field(alias="s")


class Broadcaster(BaseModel):
    seq: int
    disp: str
    scope: Literal["home", "away", "can", "natl"]
    type: Literal["tv", "radio"]
    language: Literal["English"] = Field(alias="lan")
    url: Optional[str]  # urlparse into ParseResult?


class Broadcast(BaseModel):
    broadcast: list[Broadcaster] = Field(alias="b")


class Game(BaseModel):
    gid: str
    gcode: str
    series_summary: str = Field(alias="seri")
    game_date: date = Field(alias="gdte")
    arena: str = Field(alias="an")
    city: str = Field(alias="ac")
    state: str = Field(alias="as")
    game_status: str = Field(alias="stt")
    eastern_time: datetime = Field(alias="etm")
    broadcasting: Broadcast = Field(alias="bd")
    visiting_team: Team = Field(alias="v")
    home_team: Team = Field(alias="h")
    game_date_utc: date = Field(alias="gdtutc")
    game_time_utc: time = Field(alias="utctm")


class MonthSchedule(BaseModel):
    month: str = Field(alias="mon")
    games: list[Game] = Field(alias="g")


class LeagueSchedule(BaseModel):
    month_schedule: list[MonthSchedule] = Field(alias="mscd")

    class Config:
        allow_population_by_field_name = True


YEAR = 2022
url_2022_2023_schedule = f"https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{YEAR}/league/00_full_schedule.json"

response: Response = get(url_2022_2023_schedule)

# todo: error handling
schedule: dict = response.json()

league_schedule = LeagueSchedule(
    month_schedule=[month["mscd"] for month in schedule["lscd"]]
)

SPECIAL_SYMBOLS: dict[str, str] = {"Celtics": "🍀", "Pacers": "🏎️"}


def date_from_string(start_date_str: str) -> datetime:
    good_datetime, _ = start_date_str.split(".")
    return datetime.strptime(good_datetime, "%Y-%m-%dT%H:%M:%S")


schedule_db = cast(Any, notion.client.databases.query(database_id=SCHEDULE_DATABASE_ID))

schedule_db_again = notion.client.databases.query(
    database_id=SCHEDULE_DATABASE_ID, start_cursor=schedule_db["next_cursor"]
)

beginning_of_today = datetime.combine(datetime.now(), time())


def clear_db_in_future():
    database_rows = schedule_db["results"]

    for row in database_rows:
        start_date_str: str = row["properties"]["Date"]["date"]["start"]
        game_date = date_from_string(start_date_str)

        if (
            "NBA" in row["properties"]["League"]["rich_text"][0]["plain_text"]
            and game_date > beginning_of_today
        ):
            # todo: make this check for duplicates, maybe look at return from delete?
            notion.client.blocks.delete(block_id=row["id"])


def fetch_only_future_games():
    # todo: use this for clearing only new games
    filter = {
        "property": "Date",
        "date": {"on_or_after": beginning_of_today.strftime("%Y-%m-%dT%H:%M:%S")},
    }
    x = notion.client.databases.query(database_id=SCHEDULE_DATABASE_ID, filter=filter)
    # import pdb; pdb.set_trace()

    # exit()


def recursive_fetch_and_delete(next_cursor=None):
    database_response = cast(
        Any,
        notion.client.databases.query(
            database_id=SCHEDULE_DATABASE_ID, next_cursor=next_cursor
        ),
    )
    database_rows = database_response["results"]
    for row in database_rows:
        notion.client.blocks.delete(block_id=row["id"])

    if database_response["has_more"]:
        recursive_fetch_and_delete(database_response["next_cursor"])


def clear_db_totally():
    recursive_fetch_and_delete()


clear_db_totally()

# database_rows = schedule_db['results']

# pp([row['id'] for row in database_rows])
# exit()


def assemble_matchup(game: Game, visitors_first=True) -> str:
    team_names = [game.visiting_team.team_name, game.home_team.team_name]
    if not visitors_first:
        team_names.reverse()

    for n, team_name in enumerate(team_names):
        if SPECIAL_SYMBOLS.get(team_name):
            team_name = f"{team_name} {SPECIAL_SYMBOLS[team_name]}"
        team_names[n] = team_name

    return " @ ".join(team_names)


def format_date(game: Game) -> str:
    return game.eastern_time.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )  # todo fix this from saying UTC in Notion


BROADCASTER_BADLIST = ["NBA TV"]

for month in league_schedule.month_schedule:
    for game in month.games:
        if game.eastern_time > beginning_of_today:
            for broadcaster in game.broadcasting.broadcast:
                if (
                    broadcaster.type == "tv"
                    and broadcaster.scope == "natl"
                    and broadcaster.disp not in BROADCASTER_BADLIST
                ):
                    pp(game.game_date)

                    raw_props: list[NotionProp] = [
                        {
                            "name": "Matchup",
                            "type": "title",
                            "content": assemble_matchup(game),
                        },
                        {"name": "Date", "type": "date", "content": format_date(game)},
                        {
                            "name": "Network",
                            "type": "rich_text",
                            "content": broadcaster.disp,
                        },
                        {"name": "League", "type": "rich_text", "content": "NBA"},
                        {"name": "Sport", "type": "rich_text", "content": "🏀"},
                    ]

                    props = notion.assemble_props(raw_props)

                    notion.client.pages.create(
                        parent={"database_id": SCHEDULE_DATABASE_ID}, properties=props
                    )
