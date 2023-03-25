#!/bin/sh
export PYENV_VERSION=3.9.5

# it appears ESPN starts serving the current day's games at 11am, so this needs to be run again separately at that time
echo "NHL"
poetry run python3 app/nhl_schedule.py >logs/nhl_schedule.log 2>&1
echo "Done"