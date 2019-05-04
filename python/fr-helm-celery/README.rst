fr-helm-celery Readme
=====================

Implementation
--------------

Celery Helm Processor
---------------------

INITIAL CODE / DEV ENVIRONMENT

cd fr-helm-celery

make build
Builds the required images

make compose-run

docker-run execs into running container which is running Flask in dev mode.

Go to localhost:5005/tasks

Click on a helm task set to process it with celery.

When done - returns status

Develop code on your local system - this is the code mounted into the running containers for docker or compose.

make compose-clean for teardown

Go to localhost:5555 flower to see the 1 (or 3 for compose) task queues - read debug for tasks etc.
