from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel

LOCAL_ZIP_CODE = "46203"


class Audience(BaseModel):
    id: str
    match: Literal["NONE", "ANY"]


class ViewingPolicy(BaseModel):
    actions: list[str]
    audience: Audience

    def black_out_policy_id(self) -> Optional[str]:
        is_positive_blackout_policy = "reject_blackout" in self.actions
        should_match = self.audience.match == "ANY"

        if is_positive_blackout_policy and should_match:
            return self.audience.id

        return None


class Policy(BaseModel):
    viewingPolicies: list[ViewingPolicy]

    def black_out_policy_ids(self) -> list[Optional[str]]:
        return [
            viewing_policy.black_out_policy_id()
            for viewing_policy in self.viewingPolicies
            if viewing_policy.black_out_policy_id()
        ]


class Airing(BaseModel):
    # note: an Airing represents either the home or away broadcast being shown on ESPN+
    policy: Policy

    def black_out_policy_ids(self) -> list[Optional[str]]:
        return self.policy.black_out_policy_ids()


class Event(BaseModel):
    gamecastAvailable: bool
    playByPlayAvailable: bool
    commentaryAvailable: bool
    recent: bool
    id: str
    competitionId: str
    uid: str
    date: datetime
    timeValid: bool
    name: str
    shortName: str
    location: str
    season: int
    seasonStartDate: datetime
    seasonEndDate: datetime
    seasonType: str
    seasonTypeHasGroups: bool
    group: dict
    period: int
    clock: str
    status: str
    summary: str
    fullStatus: dict
    link: str
    links: list[dict]
    onWatch: bool
    broadcasts: list[dict]
    broadcast: str
    seriesSummary: Optional[str]
    odds: dict
    competitors: list[dict]
    situation: Optional[dict]
    appLinks: list[dict]
    airings: Optional[list[Airing]]

    def black_out_policy_ids(self) -> list[Optional[str]]:
        if not self.airings:
            return []

        policy_ids = [
            airing.black_out_policy_ids()
            for airing in self.airings
            if airing.black_out_policy_ids()
        ]

        return list(set([id for sublist in policy_ids for id in sublist]))


class League(BaseModel):
    id: str
    uid: str
    name: Literal["National Hockey League"]
    abbreviation: Literal["NHL"]
    shortName: Literal["NHL"]
    slug: Literal["nhl"]
    isTournament: bool
    events: list[Event]
    smartdates: list[str]


class Sport(BaseModel):
    id: str
    uid: str
    name: str
    slug: Literal["hockey"]
    leagues: list[League]


class DailyEspnPlusNhlSchedule(BaseModel):
    sports: list[Sport]
    zipcodes: dict

    @property
    def games(self) -> list[Event]:
        # because we request 1 sport and 1 league, we can just use index to find nhl
        return self.sports[0].leagues[0].events

    def is_game_blacked_out(self, game: Event) -> bool:
        return any(
            [
                id
                for id in game.black_out_policy_ids()
                if self.zipcodes.get(id)
                and LOCAL_ZIP_CODE in (self.zipcodes.get(id) or [])
            ]
        )

    def usable_games(self) -> list[Event]:
        not_blacked_out_games: list[Event] = []
        for game in self.games:
            blacked_out = self.is_game_blacked_out(game)
            power_play_game = game.broadcast == "NHLPP|ESPN+"

            if power_play_game and not blacked_out:
                not_blacked_out_games.append(game)
        return not_blacked_out_games
