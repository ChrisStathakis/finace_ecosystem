FROM python:3.10-slim

RUN mkdir -p /home/app/
RUN mkdir -p /home/app/static/

WORKDIR /home/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build tools and compilers
RUN apk add --no-cache \
    build-base \
    gfortran \
    lapack-dev \
    cython \
    py3-pip \
    openblas-dev \
    && pip install --upgrade pip

# Install PyTorch (CPU only)
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN apk update && apk add libpq

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .