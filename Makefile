folder=$(shell basename $(CURDIR))

clear-nuxt:
	rm -rf ./front/.nuxt

clear-front: clear-nuxt
	docker volume rm -f ${folder}_node_modules

clear-db:
	docker volume rm -f ${folder}_db_data

clear: clear-front clear-db


######################## LOCAL ENVIRONMENT #############################

build:
	docker compose -f docker-compose.yml --env-file ./secret/.env build

up:
	docker compose -f docker-compose.yml --env-file ./secret/.env up

up-back:
	docker compose -f docker-compose.yml --env-file ./secret/.env up -d

down:
	docker compose -f docker-compose.yml --env-file ./secret/.env down

bash-back:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back bash

bash-front:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm front sh

migrate:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back alembic upgrade head

seed:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back bash -c "export PYTHONPATH=. && python ./app/seeder.py"

isort:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back isort --skip alembic --profile black .

flake8:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back flake8 app

black:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back black --check --diff --extend-exclude alembic --line-length 120 .

prettier:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm front yarn format:write

lint: black isort flake8 prettier

install: down clear build migrate seed down up


######################## PRODUCTION ENVIRONMENT #############################
