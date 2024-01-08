#/bin/bash

docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY  qt5-eeg-filter:latest
