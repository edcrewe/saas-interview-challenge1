from flask_restplus import Api

from fr_helm_celery.apis.helm import chart_api

api = Api(
    version="1.0",
    title="FR Helm Service",
    description="Helm Service for scheduling helm tasks via a REST API",
)

api.add_namespace(chart_api, path="/v1/chart")
