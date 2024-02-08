#!/bin/bash

apt update -y;
apt install -y curl python3 python3-pip python3-pyqt5
pip3 install poetry
cd ../
export PATH=$PATH:$HOME/.local/bin
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
poetry config virtualenvs.in-project true
poetry install


