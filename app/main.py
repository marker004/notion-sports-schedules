#!/usr/bin/env /Users/mark/Library/Caches/pypoetry/virtualenvs/sports-schedules-10zX25Yy-py3.9/bin/python

from datetime import datetime

from f1_schedule import schedule_f1
from indycar_schedule import schedule_indycar
from manual_additions import schedule_manual_events
from mlb_schedule import schedule_mlb
from nba_schedule import schedule_nba
from nhl_schedule import schedule_nhl
from soccer_schedule import schedule_soccer
from ncaa_bball_schedule import schedule_ncaa_bball

from ncaa_bball_tournament_schedule import schedule_march_madness

format = "%m/%d/%Y, %H:%M:%S"

start = datetime.now()
print(f"started: {start.strftime(format)}")
schedule_f1()
schedule_indycar()
schedule_mlb()
schedule_nba()
schedule_nhl()
schedule_soccer()
schedule_ncaa_bball()
schedule_manual_events()
schedule_march_madness()


end = datetime.now()
elapsed = end - start
print(f"finished: {end.strftime(format)}")
print(f"elapsed: {elapsed.total_seconds()} seconds")
