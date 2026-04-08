COMPOSE_LOCAL := docker-compose.local.yaml
include .env

build-loc:
	docker compose -f $(COMPOSE_LOCAL) build

up:
	docker compose -f $(COMPOSE_LOCAL) up

up-d:
	docker compose -f $(COMPOSE_LOCAL) up -d

loc:
	@make build-loc
	@make up

loc-d:
	@make build-loc
	@make up-d

exec:
	docker compose -f $(COMPOSE_LOCAL) exec api bash

makemigrations:
	docker compose -f $(COMPOSE_LOCAL) exec -it api bash -c "python manage.py makemigrations"

migrate:
	docker compose -f $(COMPOSE_LOCAL) exec -it api bash -c "python manage.py migrate"

exec-db:
	docker compose -f $(COMPOSE_LOCAL) exec -it db bash -c "export PGPASSWORD=$(POSTGRES_PASSWORD) && psql -U $(POSTGRES_USER) $(POSTGRES_DB)"

down:
	docker compose -f $(COMPOSE_LOCAL) down

cleanup:
	- docker rm -f `docker ps -aq`
	docker system prune -af

clean-db:
	@make down
	docker volume ls -q | grep $(COMPOSE_PROJECT_NAME)_nemuriya-db-data | xargs docker volume rm ;
