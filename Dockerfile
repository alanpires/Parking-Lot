# imagem base
FROM python:3.9

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

WORKDIR /code
COPY . /code/