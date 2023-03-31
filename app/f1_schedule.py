from requests import Response, get

from bs4 import BeautifulSoup

from models.f1 import F1Race, F1Response
from shared import ElligibleSportsEnum, NotionScheduler, NotionSportsScheduleItem
from utils.assemblers import F1Assembler
from shared_items.utils import measure_execution


@measure_execution("fetching new F1 schedule")
def fetch_schedule_response() -> Response:
    f1_url = "https://www.espn.com/f1/schedule"
    return get(f1_url)


def assemble_usable_games(response: Response) -> list[F1Race]:
    f1_html_doc = response.text

    soup = BeautifulSoup(f1_html_doc, "html.parser")

    f1_response = F1Response(
        race_elements_container=soup.find("table", {"class": "Table"})
    )
    return f1_response.usable_races


def assemble_notion_items(races: list[F1Race]) -> list[NotionSportsScheduleItem]:
    return [F1Assembler(race).notion_sports_schedule_item() for race in races]


response = fetch_schedule_response()
usable_races = assemble_usable_games(response)
fresh_items = assemble_notion_items(usable_races)

NotionScheduler(ElligibleSportsEnum.F1.value, fresh_items).schedule_them_shits()
