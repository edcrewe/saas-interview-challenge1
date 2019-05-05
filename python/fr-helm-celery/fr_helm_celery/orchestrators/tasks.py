"""Celery tasks - note that all args to celery must be serialisable
   These tasks are called by the REST API calls
"""
from fr_helm_celery.orchestrators import celery
from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller
import time


@celery.task(name="tasks.stub")
def longtime_add(x, y):
    print("long time task begins")
    # sleep 2 seconds
    time.sleep(2)
    print("long time task finished")
    return x + y


@celery.task(name="tasks.chart_install")
def chart_install(chart_data):
    """Sample asynchronous task. Install a helm chart on a host"""
    chart = ChartBuilder(
        {
            "name": chart_data["name"],
            "source": {
                "type": chart_data["source_type"],
                "location": chart_data["source_location"],
            },
        }
    )
    if "dry_run" in chart_data:
        dry_run = True
    else:
        dry_run = False
    tiller = Tiller(chart_data["host"])
    tiller.install_release(
        chart.get_helm_chart(), dry_run=dry_run, namespace=chart_data["namespace"]
    )


@celery.task(name="tasks.tiller_list")
def tiller_list(tiller_data):
    """Second sample task to pull back release metadata from a host"""
    tiller = Tiller(tiller_data["host"])
    data = tiller.list_releases(
        status_codes=tiller_data["status_codes"], namespace=tiller_data["namespace"]
    )
    return data
