# syntax=docker/dockerfile:1
FROM python:3
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/