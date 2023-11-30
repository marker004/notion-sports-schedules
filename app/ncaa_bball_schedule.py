from requests import Response, get

from bs4 import BeautifulSoup
from constants import TAB

from models.ncaa_game import NcaaGame, NcaaResponse
from shared import ElligibleSportsEnum, NotionSportsScheduleItem, log_good_networks
from utils import NotionScheduler
from utils.assemblers import NcaaBasketballAssembler
from shared_items.utils import measure_execution, try_it


# Only today for now
@measure_execution(f"{TAB}fetching new NCAA Basketball schedule")
def fetch_schedule_response() -> Response:
    url = "https://www.espn.com/mens-college-basketball/schedule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    }
    return get(url, headers=headers)


def assemble_usable_events(response: Response) -> list[NcaaGame]:
    html_doc = response.text

    soup = BeautifulSoup(html_doc, "html.parser")

    event_response = NcaaResponse(
        elements_container=soup.find("table", {"class": "Table"})
    )

    return event_response.usable_events


def assemble_notion_items(events: list[NcaaGame]) -> list[NotionSportsScheduleItem]:
    return [
        NcaaBasketballAssembler(event).notion_sports_schedule_item() for event in events
    ]


@try_it
def schedule_ncaa_bball():
    response = fetch_schedule_response()
    usable_events = assemble_usable_events(response)
    fresh_items = assemble_notion_items(usable_events)

    log_good_networks(fresh_items)

    NotionScheduler(ElligibleSportsEnum.BASKETBALL.value, fresh_items).schedule()


if __name__ == "__main__":
    schedule_ncaa_bball()
