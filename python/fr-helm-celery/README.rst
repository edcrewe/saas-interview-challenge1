fr-helm-celery Readme
=====================

Implementation
--------------

Celery Helm Processor
---------------------

INITIAL CODE / DEV ENVIRONMENT

cd fr-helm-celery

> make build # Builds the required image based on standard dockerhub python one

> make run # Runs up 4 containers for redis, celery, flower and web API

Web UI
------

Go to http://localhost:5000 for the Swagger UI (this takes a minute to load)

This alpha version just provides the helm install and list commands as web services

chart - Install charts

tiller - Tiller releases data

status - Service asynchronous task status information

Click on chart and then 'Try it Out' then specify the chart to be installed and hit run (click on the Model tab to see default values)

Click on tiller and submit a task for listing releases

If you have tiller installed on the host machine that you are running this up on - then supply that as the host name.

A celery task id will be returned.

Go to http://localhost:5000/v1/ to see the progress or result of running the task.

Task Monitor
------------

Go to http://localhost:5555 to see the task monitor (Flower console)

Click on Tasks to check the status and if completed successfully or failed.

Click on the task id to get the returned result or exception from running a particular task.

The Monitor tab provides live graphs of the load on Celery (if sufficient tasks are being pumped into the system)

Develop
-------

Develop code on your local system - this is the code mounted into the running containers for docker or compose.

Cleanup
-------

> make teardown # Takes down the compose containers

> make clean # For removing pyc and pycache plus build and test detritus
