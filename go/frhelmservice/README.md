Go version of ForgeOps Helm Service
===================================

Having written this service in Python and Celery we have more of a concrete spec.
so to help learn Golang lets try and reimplement it in Go.

So firstly lets pick a message queue / task manager in Go. Since its pointless re-inventing the wheel.

We could just use the go interface to Celery ... https://github.com/gocelery
Which would enable us to use go for the tasks and web UI. But this solution should be pure Golang really.

Also the system should be open source and able to use redis as a backend (ie the tasks are low traffic so redis is sufficient)

Go Task Queues with Redis backend
---------------------------------

* https://github.com/contribsys/faktory
* https://github.com/vmihailenco/taskq
* https://github.com/adjust/redismq
* https://github.com/adjust/rmq
* https://github.com/RichardKnop/machinery
* https://github.com/gocraft/work

After a quick rating based on last commit, number of commiters and features, then its between faktory and machinery.
Faktory has a built in monitor like Celery whilst machinery doesn't, but machinery has a better README and is not owned by a company,
plus I used the machinery author's Golang OAuth2 server package in the past, so lets go for machinery.

Installation
------------

The package includes a full development environment setup via docker-compose.

> cd fr-helm-service

> make help # Lists the make commands available - these wrap up the docker-compose commands for convenience

> make build # Builds the required image based on standard dockerhub Golang one

> make run # Runs up 2 containers for redis and one for machinery and web API
