#!/bin/bash
sudo apt install -y curl python3 python3-pip qt5-default
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
export PATH=$PATH:$HOME/.poetry/bin
poetry config virtualenvs.in-project true
poetry install

#python3 -m venv venv3
#venv3/bin/pip install pip --upgrade
#venv3/bin/pip install -r requirements.txt

