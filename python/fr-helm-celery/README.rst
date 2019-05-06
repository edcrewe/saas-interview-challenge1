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

.. code-block:: javascript
   {
      "name": "mariadb",
      "source_location": "https://kubernetes-charts.storage.googleapis.com/"
   }

Click on tiller and submit a task for listing releases

Note for chart install and tiller releases you need to connect to a remote version of tiller.
You will need to have TLS authentication setup for the remote Kubernetes cluster tiller and supply that to connect to it.

Hit Execute to submit the JSON payload to the API.
For whichever task you run there will be a celery task id returned.

.. code-block:: javascript
   {
      "status": "success",
      "message": "Download mariadb as task 18fbfe71-e976-4d3f-b889-e5aca82c71d3"
   }

Go to http://localhost:5000/v1/task/{task_id} to see the progress or result of running the task.

.. code-block:: javascript
   {
      "id": "c373a221-f623-4303-9531-75b3e2452ebb",
      "result": "{'name': 'mariadb',
                  'source_location': 'https://kubernetes-charts.storage.googleapis.com/',
		  'chart_location': '/tmp/pyhelm-8ke_tbu9/mariadb',
		  'yaml': 'apiVersion: v1\\nappVersion: 10.1.39\\ndescription: Fast, reliable, scalable, and easy to use open-source relational database\\n  system. MariaDB Server is intended for mission-critical, heavy-load production systems\\n  as well as for embedding into mass-deployed software. Highly available MariaDB cluster.\\nengine: gotpl\\nhome: https://mariadb.org\\nicon: https://bitnami.com/assets/stacks/mariadb/img/mariadb-stack-220x234.png\\nkeywords:\\n- mariadb\\n- mysql\\n- database\\n- sql\\n- prometheus\\nmaintainers:\\n- email: containers@bitnami.com\\n  name: Bitnami\\nname: mariadb\\nsources:\\n- https://github.com/bitnami/bitnami-docker-mariadb\\n- https://github.com/prometheus/mysqld_exporter\\nversion: 5.11.2\\n'}",
    "status": "SUCCESS"
   }

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
