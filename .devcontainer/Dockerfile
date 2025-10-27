FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Optional: install Poetry (base image already has pip, venv, git)
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
ENV PATH="/opt/poetry/bin:$PATH"

# Optional: preinstall deps
WORKDIR /workspace

CMD ["sleep", "infinity"]
