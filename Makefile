folder=$(shell basename $(CURDIR))

clear-nuxt:
	rm -rf .nuxt
	rm -rf ./front/.nuxt
	rm -rf ./front/.pnpm-store
	rm -rf ./front/.output
	rm -rf .ruff_cache
	rm -rf ./back/.ruff_cache
	rm -rf ./back/.venv

clear-front: clear-nuxt
	docker volume rm -f ${folder}_node_modules

clear-uv-cache:
	docker volume rm -f ${folder}_uv_cache

clear-db:
	docker volume rm -f ${folder}_db_data

clear: clear-front clear-uv-cache clear-db


######################## LOCAL ENVIRONMENT #############################

# install uv and nvm, `nvm install 22` for node 22
local-setup:
	rm -rf .venv && cp back/uv.lock . && cp back/pyproject.toml . && cp back/.python-version . && \
		uv sync && rm uv.lock pyproject.toml .python-version
	rm -rf node_modules && cp front/.nvmrc . && cp front/package.json . && cp front/pnpm-lock.yaml . && \
        source $(HOME)/.nvm/nvm.sh && nvm use && pnpm install && rm .nvmrc package.json pnpm-lock.yaml

uv-update: down clear-uv-cache
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back uv lock --upgrade

pnpm-update: down clear-front
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm front pnpm install --force
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm front pnpm update --latest

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
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back uv run alembic upgrade head

seed:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back bash -c "export PYTHONPATH=. && python ./app/seeder.py"

sort-imports:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back uv run ruff check --select I --fix

ruff:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm back uv run ruff format

prettier:
	docker compose -f docker-compose.yml --env-file ./secret/.env run --rm front pnpm format:write

lint: sort-imports ruff prettier

install: down clear build migrate seed down up


######################## PRODUCTION ENVIRONMENT #############################
