.PHONY: help build run lint test clean teardown

help:
	@echo "build - build docker compose image"
	@echo "run - start the flask service ready to schedule helm jobs"
	@echo "test - unit and integration tests"
	@echo "teardown - take down docker compose containers"

build:
	docker-compose build

teardown:
	docker-compose rm -f -s
	docker-compose --project-name=test down --rmi local --remove-orphans
	docker-compose --project-name=go_helm_service down --rmi local --remove-orphans
	docker volume prune -f

run: clean teardown
	docker-compose --project-name=go_helm_service up --force-recreate --no-start
	docker-compose --project-name=go_helm_service run -d -p 8000:8000 --name="fr-ops-machinery" fr-ops-machinery /bin/bash -c "cd /opt/frhelmservice/src/forgerock.com/helmservice && go build worker.go server.go && ./worker"
	docker exec -it fr-ops-machinery bash

test:
	docker-compose --project-name=test up --force-recreate --no-start
	docker-compose --project-name=test run fr-ops-machinery bash -c ""
