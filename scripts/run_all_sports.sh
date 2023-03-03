#!/bin/sh
export PYENV_VERSION=3.9.5

echo "NBA"
poetry run python3 app/nba_schedule.py >logs/nba_schedule.log 2>&1
echo "Done"
echo "Soccer"
poetry run python3 app/soccer_schedule.py >logs/soccer_schedule.log 2>&1
echo "Done"
echo "NHL"
poetry run python3 app/nhl_schedule.py >logs/nhl_schedule.log 2>&1
echo "Done"
echo "MLB"
poetry run python3 app/mlb_schedule.py >logs/mlb_schedule.log 2>&1
echo "Done"