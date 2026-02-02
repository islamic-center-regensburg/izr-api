
SEED_FILE := $(ROOT_DIR)/seed/seed_all.py

.PHONY:	seed reseed db-reset

seed:
	@PYTHONPATH=$(ROOT_DIR) uv run python $(SEED_FILE)

db-reset:
	@echo "Stopping database container..."
	make down db

	@echo "Removing database volume..."
	docker volume rm -f izr-api_db_data || true

	@echo "Starting database container..."
	make up db

reseed:
	@echo "Stopping database container..."
	make down db

	@echo "Removing database volume..."
	docker volume rm -f izr-api_db_data || true

	@echo "Starting database container..."
	make up db

	@echo "Waiting for database to be ready..."
	sleep 3

	@echo "Starting database container..."
	make db-up

	@echo "Seeding database..."
	make seed

	@echo "Database reset and seeded successfully ✅"
