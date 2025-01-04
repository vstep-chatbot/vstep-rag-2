FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS base

WORKDIR /app

COPY . .

CMD uv run app.py