# --------------------------------------
# UV / Python dependencies
# --------------------------------------

.PHONY: deps deps-sync deps-update deps-clean

deps:
	uv venv
	uv sync

deps-sync:
	uv sync

deps-update:
	uv sync --upgrade

deps-clean:
	rm -rf .venv
