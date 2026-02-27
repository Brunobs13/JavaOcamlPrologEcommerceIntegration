SHELL := /bin/bash

.PHONY: setup run test docker-up docker-down

setup:
	./scripts/setup.sh

run:
	./scripts/run_api.sh

test:
	./scripts/test.sh

docker-up:
	docker compose up --build

docker-down:
	docker compose down
