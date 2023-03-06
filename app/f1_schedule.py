from requests import Response, get

from bs4 import BeautifulSoup

from models.f1 import F1Response
from shared import ElligibleSportsEnum, clear_db_for_sport, insert_to_database
from utils.assemblers import F1Assembler
from shared_items.interfaces.notion import Notion
from shared_items.utils import measure_execution


notion = Notion()

f1_url = "https://www.espn.com/f1/schedule"

f1_response: Response = get(f1_url)

f1_html_doc = f1_response.text

soup = BeautifulSoup(f1_html_doc, "html.parser")

response = F1Response(
    race_elements_container=soup.find("table", {"class": "Table"})
)

usable_races = response.usable_races

assembled_items = [
    F1Assembler(race).notion_sports_schedule_item() for race in usable_races
]

all_props = [
    notion.assemble_props(schedule_item.format_for_notion_interface())
    for schedule_item in assembled_items
]

@measure_execution("deleting existing F1 races")
def delete_existing_races():
    clear_db_for_sport(ElligibleSportsEnum.F1.value)


delete_existing_races()


@measure_execution("inserting F1 races")
def insert_games():
    insert_to_database(all_props)


insert_games()
