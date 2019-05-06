from flask_restplus import Api

from fr_helm_celery.apis.download import download_api
from fr_helm_celery.apis.tiller import tiller_api
from fr_helm_celery.apis.chart import chart_api
from fr_helm_celery.apis.status import status_api

api = Api(
    version="1.0",
    title="ForgeRockOps Helm Service",
    description="Helm Service for scheduling helm tasks via a REST API",
)

api.add_namespace(download_api, path="/v1/download")
api.add_namespace(tiller_api, path="/v1/tiller")
api.add_namespace(chart_api, path="/v1/chart")
api.add_namespace(status_api, path="/v1/task")
