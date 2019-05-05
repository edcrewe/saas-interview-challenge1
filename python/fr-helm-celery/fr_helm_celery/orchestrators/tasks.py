"""Celery tasks - note that all args to celery must be serialisable
   These tasks are called by the REST API calls
"""
from fr_helm_celery.orchestrators import celery
import time


@celery.task(name="tasks.stub")
def longtime_add(x, y):
    print("long time task begins")
    # sleep 5 seconds
    time.sleep(5)
    print("long time task finished")
    return x + y
