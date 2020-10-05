#!/bin/bash

git stash
git pull
poetry install
#venv3/bin/pip install -r requirements.txt --upgrade