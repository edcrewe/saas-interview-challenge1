fr-helm-celery Readme
=====================

Implementation
--------------

Celery Helm Processor
---------------------

INITIAL CODE / DEV ENVIRONMENT

cd fr-helm-celery

> make build # Builds the required image based on standard dockerhub python one

> make run # Runs up redis celery and web containers

Go to localhost:5005/tasks

Click on a helm task set to process it with celery.

When done - returns status

Develop code on your local system - this is the code mounted into the running containers for docker or compose.

> make teardown # Takes down the compose containers

> make clean # For removing pyc and pycache plus build and test detritus

Go to localhost:5555 flower to see the 1 (or 3 for compose) task queues - read debug for tasks etc.
