FROM python:3.12.3-slim AS build-stage

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -

ENV PATH="/opt/poetry/bin:$PATH"
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.in-project true && poetry install --no-root

FROM python:3.12.3-slim AS runtime
ARG VERSION
ENV PATH="/opt/poetry/bin:$PATH" \
    APP_VERSION=${VERSION}

COPY --from=build-stage /opt/poetry /opt/poetry
COPY --from=build-stage /app /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends wget gnupg2 lsb-release && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget -q -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -  && \
    apt-get update && \
    apt-get install -y --no-install-recommends dialog openssh-server postgresql-client-16 && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /.cache && \
    echo "root:Docker!" | chpasswd

WORKDIR /app

COPY ./src /app/src
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY entrypoint.sh /app/entrypoint.sh
COPY sshd_config /etc/ssh/

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000 2222

ENTRYPOINT ["/app/entrypoint.sh"]
