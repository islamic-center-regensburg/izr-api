# --------------------------------------
# Main Makefile
# --------------------------------------
ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))


include scripts/make/*.mk

.DEFAULT_GOAL := help

.PHONY: help

help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-up        Start stack"
	@echo "    make docker-down      Stop stack"
	@echo "    make docker-restart   Restart stack"
	@echo "    make docker-build     Build images"
	@echo "    make docker-logs      Follow logs"
	@echo "    make docker-ps        List containers"
	@echo ""
	@echo "  Python / UV:"
	@echo "    make deps             Create venv + install deps"
	@echo "    make deps-sync        Sync from lockfile"
	@echo "    make deps-update      Upgrade deps"
	@echo "    make deps-clean       Remove venv"
	@echo ""
	@echo "  Database / Alembic:"
	@echo "    make db-rev m=\"msg\"   Create new migration"
	@echo "    make db-up             Apply migrations"
	@echo "    make db-down           Roll back last migration"
	@echo "    make db-current        Show current revision"
	@echo "    make db-history        Show migration history"
	@echo "    make db-heads          Show migration heads"
	@echo "    make db-stamp          Stamp DB with head"
	@echo ""
