FROM python:3.10-alpine

RUN mkdir -p /home/app/
RUN mkdir -p /home/app/static/

WORKDIR /home/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN apk update && apk add libpq

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .