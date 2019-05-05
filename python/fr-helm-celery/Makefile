.PHONY: help build run lint test clean

build:
	docker-compose build

help:
	@echo "build - build package (default target)"
	@echo "run - start the flask service ready to schedule helm jobs"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "lint - source code linting"
	@echo "test - unit and integration tests"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -rf .eggs
	rm -rf tests/htmlcov/
	rm -rf tests/coverage.xml
	rm -f .coverage
	rm -f unit-test-report.xml
	find . -name '*,cover' -exec rm -fr {} +

lint:
	python -m flake8 --builtins="_" --max-line-length=90 fr_helm_celery setup.py
	python -m bandit -r fr_helm_celery

test:
	docker-compose --project-name=test up --force-recreate --no-start
	docker-compose --project-name=test run fr-ops-celery bash -c '/opt/fr_helm_celery/tests/run_tests.sh'

teardown:
	docker-compose rm -f -s
	docker-compose --project-name=test down --rmi local --remove-orphans
	docker-compose --project-name=helm_service down --rmi local --remove-orphans
	docker volume prune

run:
	docker-compose --project-name=helm_service up --force-recreate --no-start
	docker-compose --project-name=helm_service run -d -p 5000:5000 -e FLASK_APP=fr_helm_celery.app -e PYTHONPATH=/opt/fr_helm_celery fr-ops-web /bin/bash -c "cd /opt/fr_helm_celery && make testdb && exec gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile=/opt/fr_helm_celery/log/gunicorn_access.log --error-logfile=/opt/fr_helm_celery/log/gunicorn_error.log --log-level=error fr_helm_celery.app:app"
