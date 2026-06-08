
COMPOSE = docker compose
EXEC_WEB = $(COMPOSE) exec web
MANAGE_PY = python manage.py

.PHONY: help up down restart build migrate populate superuser logs shell test clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart: down up

build:
	$(COMPOSE) build

migrate:
	$(EXEC_WEB) $(MANAGE_PY) migrate

populate:
	$(EXEC_WEB) $(MANAGE_PY) populate_data

superuser:
	$(EXEC_WEB) $(MANAGE_PY) createsuperuser

logs:
	$(COMPOSE) logs -f

shell:
	$(EXEC_WEB) $(MANAGE_PY) shell

test:
	$(EXEC_WEB) $(MANAGE_PY) test

init: build up migrate populate
	@echo "Project initialized. Access at http://localhost:8000"

clean:
	$(COMPOSE) down -v --rmi all --remove-orphans
