from models.soccer import GameBroadcast
from soccer_schedule import (
    League,
    Matches,
    assemble_matchup,
    fetch_league,
    format_date,
    format_network,
    format_sport,
)

from pytest import fixture


@fixture
def dummy_matches() -> Matches:
    yield Matches(
        leagues=[
            League(id=2, name="League 1"),
            League(id=879842, name="League 2"),
            League(id=1, name="League 3"),
        ]
    )


@fixture()
def dummy_broadcast_dict() -> dict:
    yield {
        "startTime": "/Date(1676821500000)/",
        "endTime": "/Date(-62135596800000)/",
        "qualifiers": ["Live"],
        "station": {
            "callSign": None,
            "stationId": "2469_st",
            "affiliateId": None,
            "affiliateCallSign": None,
            "name": "ESPN+ USA",
            "type": "Stream",
            "blockedCountryCodes": None,
        },
        "stationId": "2469_st",
        "matchId": 3900530,
        "leagueId": 879842,
        "parentLeagueId": 57,
        "program": {
            "rootId": "3900530",
            "teams": [
                {"name": "Ajax", "isHome": True, "teamBrandId": "8593"},
                {"name": "Sparta Rotterdam", "isHome": False, "teamBrandId": "8614"},
            ],
        },
        "bet365MatchId": 0,
        "externalId": "225916",
        "affiliates": [
            {
                "langCode": "en",
                "title": "Watch on ESPN+",
                "subtitle": "",
                "link": "https://go.web.plus.espn.com/c/1250707/651866/9070",
                "callToAction": "Sign Up",
                "imageUrl": "https://images.fotmob.com/image_resources/upload/ESPNplus.png",
                "disclaimer": "",
            }
        ],
        "tags": ["live"],
    }


@fixture()
def dummy_broadcast(dummy_broadcast_dict) -> GameBroadcast:
    yield GameBroadcast(**dummy_broadcast_dict)


def test_assemble_matchup(dummy_broadcast):
    assert assemble_matchup(dummy_broadcast) == "Ajax vs Sparta Rotterdam"


def test_format_date(dummy_broadcast):
    assert format_date(dummy_broadcast) == "2023-02-19T15:45:00"


def test_format_network(dummy_broadcast):
    assert format_network(dummy_broadcast) == "ESPN+ USA"


def test_format_sport():
    assert format_sport() == "⚽"


def test_fetch_league(dummy_broadcast, dummy_matches):
    assert fetch_league(dummy_broadcast, dummy_matches) == "League 2"
