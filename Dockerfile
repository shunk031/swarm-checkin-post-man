FROM python:3.11-slim as base

FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
        touch README.md && \
        pip install -U pip poetry && \
        poetry install --without dev --no-root

FROM base as runtime

ARG SCPM_PORT

ENV SCPM_PORT=${SCPM_PORT} \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY scpm ./scpm

CMD ["/bin/sh", "-c", "fastapi run scpm/run.py --port ${SCPM_PORT}"]
