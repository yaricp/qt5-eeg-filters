#/bin/bash
export DISPLAY=:0.0
xhost +
docker-compose pull
docker-compose up -d