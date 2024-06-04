from requests import Response, get
from bs4 import BeautifulSoup

from shared_items.utils import measure_execution, try_it
from constants import TAB

from models.indycar import IndycarRace, IndycarResponse
from shared import ElligibleSportsEnum, NotionSportsScheduleItem, log_good_networks
from utils import NotionScheduler

from utils.assemblers import IndycarAssembler


@measure_execution(f"{TAB}fetching new IndyCar schedule")
def fetch_schedule_response() -> Response:
    indycar_url = "https://www.espn.com/racing/schedule/_/series/indycar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    }

    return get(indycar_url, headers=headers)


def assemble_usable_events(response: Response) -> list[IndycarRace]:
    indycar_html_doc = response.text

    soup = BeautifulSoup(indycar_html_doc, "html.parser")

    indycar_response = IndycarResponse(
        race_elements_container=soup.find("table", {"class": "tablehead"})
    )
    return indycar_response.usable_events


def assemble_notion_items(races: list[IndycarRace]) -> list[NotionSportsScheduleItem]:
    return [IndycarAssembler(race).notion_sports_schedule_item() for race in races]


@try_it
def schedule_indycar():
    response = fetch_schedule_response()
    usable_events = assemble_usable_events(response)
    fresh_items = assemble_notion_items(usable_events)

    log_good_networks(fresh_items)

    NotionScheduler(ElligibleSportsEnum.INDY_CAR.value, fresh_items).schedule()


if __name__ == "__main__":
    schedule_indycar()
