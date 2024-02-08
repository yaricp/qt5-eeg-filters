#FROM jozo/pyqt5:latest
FROM ubuntu:20.04

ARG INSTALL_TZ='Asia/Novosibirsk'

RUN echo $INSTALL_TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$INSTALL_TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

RUN apt update && apt upgrade -y
RUN apt install -y curl python3-pip python3-pyqt5 bash
RUN pip3 install poetry

COPY poetry.lock  pyproject.toml ./docker/start.sh /

WORKDIR /

RUN poetry install

COPY ./src /app

ENTRYPOINT ["/usr/bin/bash", "-c"]

CMD ["./start.sh"]
