from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from constants import NHL_BROADCAST_BADLIST, HARD_TIMES_BADLIST


class Team(BaseModel):
    abbrev: str


class Broadcast(BaseModel):
    network: str

    def watchable(self) -> bool:
        return self.network not in (NHL_BROADCAST_BADLIST + HARD_TIMES_BADLIST)


class Game(BaseModel):
    startTimeUTC: datetime
    tvBroadcasts: list[Broadcast] = []
    awayTeam: Team
    homeTeam: Team
    gameState: Literal["FUT", "OFF", "LIVE"]

    def watchable_broadcasts(self) -> list[Broadcast]:
        return [broadcast for broadcast in self.tvBroadcasts if broadcast.watchable()]

    def any_watchable_broadcasts(self) -> bool:
        return any(self.watchable_broadcasts())


class GameDay(BaseModel):
    games: list[Game]


class LeagueBroadcastSchedule(BaseModel):
    gameWeek: list[GameDay]

    def usable_events(self):
        return [
            game
            for date in self.gameWeek
            for game in date.games
            if game.any_watchable_broadcasts()
        ]
