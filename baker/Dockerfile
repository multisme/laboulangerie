FROM python:3.9-slim-buster

RUN mkdir /baker
COPY . /baker/

WORKDIR /baker

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN apt-get update
RUN apt-get -y install libsodium-dev libsecp256k1-dev libgmp-dev git gcc pkg-config wget nginx


RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-root

RUN poetry shell

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
