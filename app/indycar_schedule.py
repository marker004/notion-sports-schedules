from requests import Response, get
from bs4 import BeautifulSoup

from shared_items.interfaces.notion import Notion
from shared_items.utils import measure_execution

from models.indycar import IndycarResponse
from shared import ElligibleSportsEnum, clear_db_for_sport, insert_to_database
from utils.assemblers import IndycarAssembler

notion = Notion()

indycar_url = "https://www.espn.com/racing/schedule/_/series/indycar"

indycar_response: Response = get(indycar_url)

indycar_html_doc = indycar_response.text

soup = BeautifulSoup(indycar_html_doc, "html.parser")

response = IndycarResponse(
    race_elements_container=soup.find("table", {"class": "tablehead"})
)

usable_races = response.usable_races

assembled_items = [
    IndycarAssembler(race).notion_sports_schedule_item() for race in usable_races
]

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembled_items
]

@measure_execution("deleting existing IndyCar races")
def delete_existing_races():
    clear_db_for_sport(ElligibleSportsEnum.INDY_CAR.value)


delete_existing_races()


@measure_execution("inserting IndyCar races")
def insert_games():
    insert_to_database(all_props)


insert_games()
