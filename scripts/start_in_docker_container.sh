#/bin/bash
export DISPLAY=:0.0
xhost +
if [ "${PWD##*/}" == "scripts" ]; then
  cd ../;
fi
docker compose pull
docker compose up -d