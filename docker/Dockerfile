FROM jozo/pyqt5:latest

RUN apt update && apt upgrade -y
RUN apt install -y curl python3-pip bash
RUN pip3 install poetry

COPY poetry.lock  pyproject.toml ./docker/start.sh /

WORKDIR /

RUN poetry install

COPY ./src /app

ENTRYPOINT ["/usr/bin/bash", "-c"]

CMD ["./start.sh"]
