FROM python:bookworm
USER root
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nano \
    wget \
    && pip3 install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip3 install -r requirements.txt