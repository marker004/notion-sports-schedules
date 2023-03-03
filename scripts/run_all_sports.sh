#!/bin/sh
export PYENV_VERSION=3.9.5

poetry run python3 app/nba_schedule.py >logs/nba_schedule.log 2>&1
poetry run python3 app/soccer_schedule.py >logs/soccer_schedule.log 2>&1
poetry run python3 app/nhl_schedule.py >logs/nhl_schedule.log 2>&1
poetry run python3 app/mlb_schedule.py >logs/mlb_schedule.log 2>&1