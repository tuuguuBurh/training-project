FROM python:3.13-slim-bookworm AS base

COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY ./back/uv.lock ./back/pyproject.toml /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"
