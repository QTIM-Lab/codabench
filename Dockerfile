FROM python:3.8

RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*

# Install Docker
RUN apt-get update && curl -fsSL https://get.docker.com | sh

ENV PYTHONUNBUFFERED 1

ADD requirements.dev.txt .
ADD requirements.txt .
RUN pip install --upgrade "pip<24.1"
RUN pip install -r requirements.dev.txt

WORKDIR /app
