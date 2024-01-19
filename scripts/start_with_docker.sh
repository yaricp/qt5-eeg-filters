#/bin/bash

docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix \
-v ./data:/data \
-e DISPLAY=:0.0  yaricp/qt5-eeg-filters:latest
