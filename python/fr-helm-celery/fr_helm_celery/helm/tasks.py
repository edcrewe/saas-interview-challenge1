"""Celery tasks - note that all args to celery must be serialisable
   These tasks are called by the REST API calls
"""
import time
import os

from fr_helm_celery.helm import celery
from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller
from pyhelm.repo import from_repo


@celery.task(name="tasks.stub")
def longtime_add(x, y):
    """Dummy asynchonous task"""
    print("long time task begins")
    # sleep 2 seconds
    time.sleep(2)
    print("long time task finished")
    return x + y


def get_tiller(data):
    """Use connection details for tiller as given by...
       > kubectl describe deploy tiller-deploy --namespace=kube-system
       TLS setup is required for access from outside the Kubernetes cluster
    """
    tls = data.get("tls", "")
    if tls:
        return Tiller(data["host"], port=data["port"])
    else:
        return Tiller(data["host"], port=data["port"], tls_config=tls)


@celery.task(name="tasks.chart_download")
def chart_download(data):
    """Sample asynchronous task. Download a helm chart to the cache"""
    chart = data.copy()
    chart["chart_location"] = from_repo(data["source_location"], data["name"])
    chart_path = os.path.join(chart["chart_location"], "Chart.yaml")
    if os.path.exists(chart_path):
        with open(chart_path, "r") as fh:
            chart["yaml"] = fh.read()
    return chart


@celery.task(name="tasks.tiller_list")
def tiller_list(tiller_data):
    """Second sample task to pull back release metadata from a host"""
    tiller = get_tiller(tiller_data)
    return tiller.list_releases(
        status_codes=tiller_data["status_codes"], namespace=tiller_data["namespace"]
    )


@celery.task(name="tasks.chart_install")
def chart_install(chart_data):
    """Third sample asynchronous task. Install a helm chart on a host"""
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
    tiller = get_tiller(chart_data)
    return tiller.install_release(
        chart.get_helm_chart(), dry_run=dry_run, namespace=chart_data["namespace"]
    )
