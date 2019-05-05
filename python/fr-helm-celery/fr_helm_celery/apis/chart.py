"""Helm Charts
"""
import logging
from fr_helm_celery.orchestrators import celery

from flask_restplus import Resource, Namespace, fields
from celery.exceptions import CeleryError

logger = logging.getLogger()

chart_api = Namespace("chart", description="Install charts")

chart = chart_api.model(
    "ChartMetadata",
    {
        "host": fields.String(
            required=True, description="Service host", default="localhost"
        ),
        "name": fields.String(
            required=True, description="Service name", default="nginx-ingress"
        ),
        "source_type": fields.String(
            required=True, description="Chart source type", default="repo"
        ),
        "source_location": fields.String(
            required=True,
            description="Chart source type",
            default="https://kubernetes-charts.storage.googleapis.com",
        ),
        "dry_run": fields.Boolean(
            required=False,
            default=True,
            description="Flag for dry run (omit for actual run)",
        ),
    },
)


@chart_api.route("/")
class Chart(Resource):
    """Resource for creating charts"""

    @chart_api.response(413, "Allowed payload size is 1024 bytes")
    @chart_api.response(400, "Chart validation error")
    @chart_api.response(202, "Chart accepted for submission")
    @chart_api.expect(chart, validate=True)
    def post(self):
        chart_data = chart_api.payload
        if chart_data["name"]:
            try:
                task = celery.send_task("tasks.chart_install", args=[chart_api.payload])
                logger.info("Helm install start task %s", task.id)
            except CeleryError:
                logger.critical(
                    "Logging start task failed due to celery error", exc_info=True
                )

                return (
                    {
                        "status": "error",
                        "message": "Unable to start chart install task",
                    },
                    500,
                )
        return {
            "status": "success",
            "message": "Installing chart {} as task {}".format(
                chart_data["name"], task.id
            ),
        }
