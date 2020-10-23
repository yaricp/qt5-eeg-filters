#!/bin/bash
sudo apt install -y curl python3 python3-pip qt5-default
pip3 install poetry
export PATH=$PATH:$HOME/.local/bin
poetry config virtualenvs.in-project true
poetry install


