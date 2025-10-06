#!/bin/bash

sudo apt update -y;
sudo apt install -y curl python3 python3-pip python3-pyqt5;
pip3 install poetry;
if [ "${PWD##*/}" == "scripts" ]; then
  cd ../;
fi
export PATH=$PATH:$HOME/.local/bin;
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc;
echo "start creating lock file"
poetry lock;
echo "config poetry";
poetry config virtualenvs.in-project true;
echo "install packages";
poetry install --no-root;


