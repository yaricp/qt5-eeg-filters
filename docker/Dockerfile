FROM ubuntu:24.04

RUN apt update && apt upgrade -y
RUN apt install -y curl python3.12 python3-poetry python3-pyqt5 bash qt5-qmake
RUN apt install -y xvfb
COPY poetry.lock  pyproject.toml ./docker/start.sh /

WORKDIR /

RUN poetry lock
RUN poetry install --no-root

# Set up Xvfb
# RUN echo "Xvfb :1 -screen 0 1024x768x16 &" >> /etc/X11/Xsession

COPY ./src /app

ENTRYPOINT ["/usr/bin/bash", "-c"]

CMD ["./start.sh"]
