FROM python:3.11-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md /app/
COPY src/ /app/src/

RUN uv sync --frozen --no-cache

ARG SCPM_PORT
CMD ["/bin/sh", "-c", "/app/.venv/bin/fastapi run src/scpm/run.py --port ${SCPM_PORT}"]
