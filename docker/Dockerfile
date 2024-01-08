FROM jozo/pyqt5:latest

RUN apt update && apt upgrade -y
RUN apt install -y curl python3-pip bash
RUN pip3 install poetry

COPY poetry.lock  pyproject.toml /app/
COPY ./src /app
COPY ./docker/start.sh /app

RUN export PATH=$PATH:$HOME/.local/bin && echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
RUN poetry config virtualenvs.in-project true

WORKDIR /app

RUN poetry install

ENTRYPOINT ["/usr/bin/bash", "-c"]

CMD ["./start.sh"]
