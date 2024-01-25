#/bin/bash

docker build -f ../docker/Dockerfile -t yaricp/qt5-eeg-filters:latest ../
docker push yaricp/qt5-eeg-filters:latest

docker tag yaricp/qt5-eeg-filters:latest ghcr.io/yaricp/qt5-eeg-filters:latest
docker push ghcr.io/yaricp/qt5-eeg-filters:latest