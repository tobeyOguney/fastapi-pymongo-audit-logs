FROM python:3.10.0-buster

RUN pip install poetry
WORKDIR /code

COPY pyproject.toml /code/
RUN poetry install && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY service/ /code/service
