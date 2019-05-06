.PHONY: help build run lint test clean teardown

help:
	@echo "build - build docker compose image"
	@echo "run - start the flask service ready to schedule helm jobs"
	@echo "lint - source code linting"
	@echo "test - unit and integration tests"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "teardown - take down docker compose containers"

build:
	docker-compose build

teardown:
	docker-compose rm -f -s
	docker-compose --project-name=test down --rmi local --remove-orphans
	docker-compose --project-name=helm_service down --rmi local --remove-orphans
	docker volume prune -f

run: clean teardown
	docker-compose --project-name=helm_service up --force-recreate --no-start
	docker-compose --project-name=helm_service run -d -p 5000:5000 -e FLASK_APP=fr_helm_celery.app -e PYTHONPATH=/opt/fr-helm-celery/fr_helm_celery fr-ops-web /bin/bash -c "pip install -Ur /opt/fr-helm-celery/requirements/web.txt && cd /opt/fr-helm-celery && exec gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile=/var/log/gunicorn_access.log --error-logfile=/var/log/gunicorn_error.log --log-level=error fr_helm_celery.app:app"

lint:
	docker-compose --project-name=test up --force-recreate --no-start
	docker-compose --project-name=test run fr-ops-celery bash -c "python -m flake8 --builtins="_" --max-line-length=90 fr_helm_celery setup.py"
	docker-compose --project-name=test run fr-ops-celery bash -c "python -m bandit -r fr_helm_celery"

test:
	docker-compose --project-name=test up --force-recreate --no-start
	docker-compose --project-name=test run fr-ops-celery bash -c '/opt/fr-helm-celery/tests/runner.sh'

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -rf .eggs
