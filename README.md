# izr-api

## Overview

`izr-api` is a containerized backend project designed for local development and production parity. The project uses:

* **Docker Compose** for service orchestration
* **Makefiles** for a simple, consistent developer interface
* **uv** for fast Python dependency management
* **Alembic** for database migrations

The goal is to ensure that **every developer can get started with a single command** and use the same workflows locally, in CI, and in production-like environments.

---

## Project Structure

```text
.
├── docker-compose.yaml        # Root compose file (includes others)
├── docker/                    # Compose fragments (api, db, etc.)
├── scripts                    # Modular makefiles
    └─ make/
│      ├── docker.mk           # Docker / Compose commands
│      ├── uv.mk               # Python / uv dependency commands
│      └── alembic.mk          # Database migration commands
├── pyproject.toml             # Python project definition
├── alembic.ini                # Alembic configuration
└── Makefile                   # Main entry point (includes all .mk files)
```

---

## Getting Started

### 1. Prerequisites

Make sure you have the following installed:

* Docker + Docker Compose (v2)
* GNU Make
* Python 3.10+
* `uv`

---

### 2. Install Python dependencies

```bash
make deps
```

Or, if using a lockfile:

```bash
make deps-sync
```

This will create a `.venv/` directory in the project root.

---

### 3. Start the full stack

```bash
make up
```

This starts **all services** defined in Docker Compose.

To start only specific services:

```bash
make up api
make up db
make up api db
```

---

## Docker Commands

Common Docker workflows are wrapped in Make targets.

```bash
make up              # Start all services
make down            # Stop the stack
make restart         # Restart services
make build           # Build images
make logs             # Follow logs (all)
make logs api         # Logs for one service
make ps               # List running containers
```

Service names can always be passed as arguments.

---

## Database & Migrations (Alembic)

All database migration workflows are standardized.

### Create a new migration

```bash
make db-rev m="add users table"
```

### Apply migrations

```bash
make db-up
```

### Roll back one migration

```bash
make db-down
```

### Inspect migration state

```bash
make db-current
make db-history
make db-heads
```

### Fix DB state (advanced)

```bash
make db-stamp
```

---

## Help

At any time, you can run:

```bash
make help
```

This prints all available commands grouped by category.

---

## Development Guidelines

* **Do not run docker-compose manually** — use `make`
* **Do not edit the root Makefile** for features; add new `.mk` files instead
* Keep targets small, explicit, and predictable

---

## Extending the Project

The setup is designed to scale cleanly. Future additions may include:

* `lint.mk` (ruff, black, mypy)
* `test.mk` (pytest)
* `ci.mk` (CI-specific targets)
* Multiple environments (dev / staging / prod)

---

## Summary

This project prioritizes:

* Consistency over cleverness
* Simple commands over documentation-heavy workflows
* A single source of truth for development tasks

If you know `make`, you know the project.
