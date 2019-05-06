fr-helm-celery Readme
=====================

Celery Helm Python Package

Installation
------------

The package includes a full development environment setup via docker-compose.

> cd fr-helm-celery

> make help # Lists the make commands available - these wrap up the docker-compose commands for convenience

> make build # Builds the required image based on standard dockerhub python one

> make run # Runs up 4 containers for redis, celery, flower and web API

These containers include the package itself installed via

pip install -e fr-helm-celery

Web UI
------

Go to http://localhost:5000 for the Swagger UI (this takes a minute to load)

This alpha version just provides some sample helm commands. Chart download, install and list releases as web services

download - Downloads a chart to the local cache

tiller - Tiller releases data

chart - Install charts

status - Service asynchronous task status information

Click on download and then 'Try it Out' then specify the chart to be downloaded and hit run (click on the Model tab to see default values)

|   {
|      "name": "mariadb",
|      "source_location": "https://kubernetes-charts.storage.googleapis.com/"
|   }


Click on tiller and submit a task for listing releases

Note for chart install and tiller releases you need to connect to a remote version of tiller.
You will need to have TLS authentication setup for the remote Kubernetes cluster tiller and supply that to connect to it.

Hit Execute to submit the JSON payload to the API.
For whichever task you run there will be a celery task id returned.

|   {
|      "status": "success",
|      "task_id": "18fbfe71-e976-4d3f-b889-e5aca82c71d3",
|      "message": "Download mariadb as task 18fbfe71-e976-4d3f-b889-e5aca82c71d3"
|   }


Go to http://localhost:5000/v1/task/{task_id} to see the progress or result of running the task.

|   {
|      "id": "c373a221-f623-4303-9531-75b3e2452ebb",
|      "result": "{'name': 'mariadb',
|                  'source_location': 'https://kubernetes-charts.storage.googleapis.com/',
|		  'chart_location': '/tmp/pyhelm-8ke_tbu9/mariadb',
|		  'yaml': 'apiVersion: v1\\nappVersion: 10.1.39\\ndescription: Fast, reliable, scalable, and easy to use open-source relational database\\n  system. MariaDB Server is intended for mission-critical, heavy-load production systems\\n  as well as for embedding into mass-deployed software. Highly available MariaDB cluster.\\nengine: gotpl\\nhome: https://mariadb.org\\nicon: https://bitnami.com/assets/stacks/mariadb/img/mariadb-stack-220x234.png\\nkeywords:\\n- mariadb\\n- mysql\\n- database\\n- sql\\n- prometheus\\nmaintainers:\\n- email: containers@bitnami.com\\n  name: Bitnami\\nname: mariadb\\nsources:\\n- https://github.com/bitnami/bitnami-docker-mariadb\\n- https://github.com/prometheus/mysqld_exporter\\nversion: 5.11.2\\n'}",
|    "status": "SUCCESS"
|   }


Task Monitor
------------

Go to http://localhost:5555 to see the task monitor (Flower console)

Click on Tasks to check the status and if completed successfully or failed.

Click on the task id to get the returned result or exception from running a particular task.

The Monitor tab provides live graphs of the load on Celery (if sufficient tasks are being pumped into the system)

Develop
-------

Develop code in fr-helm-celery on your local system - this is the code mounted into the running containers for docker or compose.

If you want to see changes instantly for the web API code - with the log to stdout, then you may want to run up the Flask dev server instead of gunicorn.

You can run up the web container to sleep and then exec in to run Flask interactively...

-  make teardown
-  docker-compose --project-name=dev_helm up --force-recreate --no-start
-  docker-compose --project-name=dev_helm run -d -p 5000:5000 -e FLASK_APP=fr_helm_celery.app -e PYTHONPATH=/opt/fr-helm-celery/fr_helm_celery --name=dev_helm_web fr-ops-web /bin/bash -c "pip install -Ur /opt/fr-helm-celery/requirements/web.txt && sleep 1d"
-  docker exec -it dev_helm_web bash
-  root@f2cd7f344bcb:/# cd /opt/fr-helm-celery && flask run -h 0.0.0.0

You will see any requests coming in via http://localhost:5000 on the console.

NOTE: If you use make run then you will need to restart the container for code changes to be seen in gunicorn (restart web) or in celery (restart celery).

Linting
-------

> make lint

Runs Flake8 and Bandit on the celery container which has the source package mounted to it at /opt/fr-helm-celery
This confirms that the code has no badly formatted code or python usage security issues
It will also pick up unused imports etc.

Note: The code is black formatted (the equivalent of golang's fmt)

See this presentation for details https://docs.google.com/presentation/d/1rpQlJTv9uBWicuu2cQURG1Yfu-j4cK-EDd9LwbD-SdA/edit?usp=sharing


Tests
-----

> make test

Runs the unit and integration test suite.


Cleanup
-------

> make teardown # Takes down the compose containers

> make clean # For removing pyc and pycache plus build and test detritus

Questions
---------

**Are there any shortcomings of the code?**

- There is no authorisation system implemented.
- The design of the REST API is somewhat arbitary based on picking a few sample commands.
- There is only a single test/dev Flask config. For production at least a config with enforced HTTPS would be needed and an SSL proxy in front of gunicron or use of Apache mod_wsgi or some other more secure web server setup.
- Submitting the TLS authorisation for connecting to remote Tiller instances via JSON is questionable and certainly shouldnt be done without having authorisation and HTTPS in place.
- The Chart download to local pyhelm cache and path should be surfaced as a managed cache for use in combination with the install, otherwise its a little pointless - since we might as well always use repo and URL for the chart install type and source rather than use these cached Charts
- CeleryBeat tasks could be setup to cater for scheduled task running.
- Using redis as the Celery backend can cause a bottleneck if a sufficient number of requests are pushed in.

**How might this project be scaled?**

- Move the Celery broker from redis to one of the more scalable ones: Rabbit MQ, Amazon SQS or perhaps Zookeeper
- Scale out by simply adding more celery workers per celery instance and more instance containers
- Analyse the realworld usage and at least optimize the tasks and task flows for it.
- Add a central persistent data store to hold cluster state and metadata - to better inform required commands and perhaps add a higher level business logic API over them, eg. command payload becomes rollback US-123 idm to vers-456 - instead of direct helm commands.

**How might one approach doing sequential versus parallel tasks?**

Common approaches are to either use a lock so that a task is only run when it is acquired.
Or to chain tasks together so that successful completion of one is used as callback to the next.

Celery offers various primitives for creating complex parallel and serial flows of task execution. Since each of the primitives can call the others, see the canvas documentation http://docs.celeryproject.org/en/latest/userguide/canvas.html
Some examples of the primitives are as follows...

- Group provides standard parallel execution.
- Chain links together tasks making a chain of callbacks. So that each task is only enabled for execution after completion of the previous one.
- Chord is basically a Group with a final task that only gets run after the group tasks have all completed their parallel run.
- Map runs a task repeatedly with a list of different arguments returning all the results or an aggregation of them.
