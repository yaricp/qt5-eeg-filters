#!/bin/bash

git stash
git pull
venv3/bin/pip install -r requirements.txt --upgrade