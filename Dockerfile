# ----------------------------
# Build stage
# ----------------------------
FROM python:3.12.3-slim AS build-stage

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTE=1 \
    UV_LINK_MODE=copy

# Copy uv binary (no install script)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv .venv && \
    uv sync --frozen

# ----------------------------
# Runtime stage
# ----------------------------
FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=build-stage /app /app

# System deps (unchanged)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget gnupg2 lsb-release \
    && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
    > /etc/apt/sources.list.d/pgdg.list \
    && wget -q -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && \
    apt-get install -y --no-install-recommends \
    dialog openssh-server postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

COPY ./src /app/src
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY entrypoint.sh /app/entrypoint.sh
COPY gunicorn.conf.py /app/gunicorn.conf.py
COPY sshd_config /etc/ssh/

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000 2222

ENTRYPOINT ["/app/entrypoint.sh"]
