#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sh ./scripts/linux/install.sh;
    cp .env_linux .env;
elif [[ "$OSTYPE" == "darwin"* ]]; then
    sh ./scripts/macos/install.sh;
    cp .env_macos .env;
elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "cygwin not supported yet!"
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "msys not supported yet!"
elif [[ "$OSTYPE" == "win32" ]]; then
    echo "win32 not supported yet!"
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    echo "freebsd not supported yet!"
fi

docker compose pull;
export DISPLAY=:0.0 ;
xhost + ;
docker compose up -d;
