from models.soccer import GameBroadcast, LeagueTypes, League, Matches
from shared import ElligibleSportsEnum

from utils.assemblers import SoccerAssembler

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


@fixture
def dummy_leagues_primary() -> LeagueTypes:
    yield LeagueTypes(
        international=[
            {
                "name": "INT",
                "leagues": [
                    {"name": "World Cup", "id": 2},
                    {"name": "Euro Cup", "id": 879842},
                ],
            }
        ],
        countries=[
            {
                "name": "Wakanda",
                "leagues": [
                    {"name": "BP Premiere League", "id": 3},
                    {"name": "BP Second League", "id": 4},
                ],
            }
        ],
    )


@fixture
def dummy_leagues_secondary() -> LeagueTypes:
    yield LeagueTypes(
        international=[
            {
                "name": "INT",
                "leagues": [
                    {"name": "World Cup", "id": 2},
                    {"name": "Euro Cup", "id": 1},
                ],
            }
        ],
        countries=[
            {
                "name": "Wakanda",
                "leagues": [
                    {"name": "BP Premiere League", "id": 57},
                    {"name": "BP Second League", "id": 4},
                ],
            }
        ],
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


def test_assemble_matchup(dummy_broadcast, dummy_leagues_primary):
    assert (
        SoccerAssembler(dummy_broadcast, dummy_leagues_primary).assemble_matchup()
        == "Ajax vs Sparta Rotterdam"
    )


def test_format_date(dummy_broadcast, dummy_leagues_primary):
    assert (
        SoccerAssembler(dummy_broadcast, dummy_leagues_primary).format_date()
        == "2023-02-19T10:45:00"
    )


def test_format_network(dummy_broadcast, dummy_leagues_primary):
    assert (
        SoccerAssembler(dummy_broadcast, dummy_leagues_primary).format_network()
        == "ESPN+ USA"
    )


def test_format_sport(dummy_broadcast, dummy_leagues_primary):
    assert (
        SoccerAssembler(dummy_broadcast, dummy_leagues_primary).format_sport()
        == ElligibleSportsEnum.SOCCER.value
    )


def test_fetch_league_by_primary_league_id(dummy_broadcast, dummy_leagues_primary):
    assert (
        SoccerAssembler(dummy_broadcast, dummy_leagues_primary).fetch_league()
        == "Euro Cup"
    )


def test_fetch_league_by_parent_league_id(dummy_broadcast, dummy_leagues_secondary):
    assert (
        SoccerAssembler(dummy_broadcast, dummy_leagues_secondary).fetch_league()
        == "BP Premiere League - Wakanda"
    )
