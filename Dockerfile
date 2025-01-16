FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS base

COPY --from=openjdk:8-jdk-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME /usr/local/openjdk-8

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

WORKDIR /app

COPY . .

RUN apt-get update &&\
  apt-get install -y wget && \
  apt-get clean

CMD uv run app.py
