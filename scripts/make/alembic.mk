# --------------------------------------
# Alembic (DB migrations)
# --------------------------------------

ALEMBIC := alembic
ALEMBIC_CFG := $(ROOT_DIR)/alembic.ini

.PHONY: \
	db-rev \
	db-up \
	db-down \
	db-current \
	db-history \
	db-heads \
	db-stamp \
	db-reset

# Create a new migration (requires message)
# Usage: make db-rev m="add users table"
db-rev:
	@if [ -z "$(m)" ]; then \
	  echo "❌ Missing migration message. Use: make db-rev m=\"message\""; \
	  exit 1; \
	fi
	$(ALEMBIC) -c $(ALEMBIC_CFG) revision --autogenerate -m "$(m)"

# Upgrade to latest
db-up:
	$(ALEMBIC) -c $(ALEMBIC_CFG) upgrade head

# Downgrade one revision
db-down:
	$(ALEMBIC) -c $(ALEMBIC_CFG) downgrade -1

# Show current revision
db-current:
	$(ALEMBIC) -c $(ALEMBIC_CFG) current

# Show full migration history
db-history:
	$(ALEMBIC) -c $(ALEMBIC_CFG) history

# Show all heads (useful for branch conflicts)
db-heads:
	$(ALEMBIC) -c $(ALEMBIC_CFG) heads

# Stamp DB with head (no migration run)
db-stamp:
	$(ALEMBIC) -c $(ALEMBIC_CFG) stamp head
