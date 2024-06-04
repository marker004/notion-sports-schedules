from requests import Response, get

from bs4 import BeautifulSoup
from constants import TAB

from models.f1 import F1Race, F1Response
from shared import ElligibleSportsEnum, NotionSportsScheduleItem, log_good_networks
from utils import NotionScheduler
from utils.assemblers import F1Assembler
from shared_items.utils import measure_execution, try_it


@measure_execution(f"{TAB}fetching new F1 schedule")
def fetch_schedule_response() -> Response:
    f1_url = "https://www.espn.com/f1/schedule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    }
    return get(f1_url, headers=headers)


def assemble_usable_events(response: Response) -> list[F1Race]:
    f1_html_doc = response.text

    soup = BeautifulSoup(f1_html_doc, "html.parser")

    f1_response = F1Response(
        race_elements_container=soup.find("table", {"class": "Table"})
    )

    return f1_response.usable_events


def assemble_notion_items(races: list[F1Race]) -> list[NotionSportsScheduleItem]:
    return [F1Assembler(race).notion_sports_schedule_item() for race in races]


@try_it
def schedule_f1():
    response = fetch_schedule_response()
    usable_events = assemble_usable_events(response)
    fresh_items = assemble_notion_items(usable_events)

    log_good_networks(fresh_items)

    NotionScheduler(ElligibleSportsEnum.F1.value, fresh_items).schedule()


if __name__ == "__main__":
    schedule_f1()
