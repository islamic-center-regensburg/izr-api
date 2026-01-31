
SEED_FILE := $(ROOT_DIR)/seed/seed_all.py

.PHONY:	seed

seed:
	@PYTHONPATH=$(ROOT_DIR) uv run python $(SEED_FILE)
