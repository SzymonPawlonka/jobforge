SHELL := /bin/bash

.PHONY: copy-env up down logs reset test test-python test-go lint proto admin seed

copy-env:
	@test -f .env || cp .env.example .env
	@echo "Plik .env gotowy. Zmień JWT_SECRET i ADMIN_PASSWORD."

up: copy-env
	docker compose up --build -d
	docker compose ps

logs:
	docker compose logs -f api analyzer db

down:
	docker compose down

reset:
	docker compose down -v --remove-orphans

admin:
	docker compose exec api python -m app.scripts.create_admin

seed:
	docker compose exec api python -m app.scripts.seed_demo

test: test-python test-go

test-python:
	cd services/api-python && pytest -q

test-go:
	cd services/analyzer-go && go test ./...

proto:
	./scripts/generate-proto.sh
