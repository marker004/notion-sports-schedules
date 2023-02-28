from urllib import parse

BOOKENDS = ["2022-10-07", "2023-4-13"]

base_url = "https://statsapi.web.nhl.com/api/v1/schedule?"

params = (
    ("startDate", BOOKENDS[0]),
    ("endDate", BOOKENDS[1]),
    ("hydrate", "broadcasts(all)"),
    ("site", "en_nhl"),
    ("teamId", ""),
    ("gameType", ""),
    ("timecode", ""),
)

assembled_url = base_url + parse.urlencode(params, safe=",()")

# url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=2023-02-14&endDate=2023-02-19&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=en_nhl&teamId=&gameType=&timecode="

# print(assembled_url)
# print(url)

# assert assembled_url == url


from itertools import groupby
from shared_items.utils import pp
from shared_items.interfaces import Notion
from requests import Response, get
from constants import SOCCER_BROADCAST_BADLIST

from models.soccer import GameBroadcast, LeagueTypes
from shared import SCHEDULE_DATABASE_ID
from utils.assemblers import SoccerAssembler

notion = Notion()

schedule_response: Response = get(assembled_url)
schedule_json: dict = schedule_response.json()

import pdb

pdb.set_trace()
