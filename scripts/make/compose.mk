# --------------------------------------
# Docker Compose configuration
# --------------------------------------

COMPOSE_FILE := $(ROOT_DIR)/docker-compose.yaml
ENV_FILE     := $(ROOT_DIR)/.docker.env
DC           := docker compose

# --------------------------------------
# Known targets
# --------------------------------------

COMMANDS := up down restart logs ps build config stop rm

SERVICE := $(filter-out $(COMMANDS),$(MAKECMDGOALS))

# --------------------------------------
# Targets
# --------------------------------------

.PHONY: $(COMMANDS)

up:
	$(DC) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up -d $(SERVICE)

down:
	$(DC) -f $(COMPOSE_FILE) down

restart:
	$(DC) -f $(COMPOSE_FILE) restart $(SERVICE)

build:
	$(DC) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) build $(SERVICE)

logs:
	$(DC) -f $(COMPOSE_FILE) logs -f $(SERVICE)

ps:
	$(DC) -f $(COMPOSE_FILE) ps $(SERVICE)

config:
	$(DC) --env-file $(ENV_FILE) -f $(COMPOSE_FILE) config

stop:
	$(DC) -f $(COMPOSE_FILE) stop $(SERVICE)

rm:
	$(DC) -f $(COMPOSE_FILE) rm -f $(SERVICE)

# --------------------------------------
# Catch-all (required)
# --------------------------------------

%:
	@:
