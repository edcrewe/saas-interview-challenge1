ForgeRock Helm Celery
=====================

PreRequisites
-------------

Machine with docker and docker-compose installed.

Getting started
---------------

> make help

build - build docker compose image
run - start the flask service ready to schedule helm jobs
lint - source code linting
test - unit and integration tests
clean - remove all build, test, coverage and Python artifacts
teardown - take down docker compose containers

So to get started you need to run

make build
make run

Go to http://localhost:5000 and try out the ForgeRockOps Helm Service
