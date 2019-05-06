"""Helm Chart Downloads
"""
import logging
from fr_helm_celery.helm import celery

from flask_restplus import Resource, Namespace, fields
from celery.exceptions import CeleryError

logger = logging.getLogger()

download_api = Namespace("download", description="Download helm charts")

download = download_api.model(
    "DownloadMetadata",
    {
        "name": fields.String(
            required=True, description="Chart name", default="mariadb"
        ),
        "source_location": fields.String(
            required=True,
            description="Download source URL",
            default="https://kubernetes-charts.storage.googleapis.com/",
        ),
    },
)


@download_api.route("/")
class Download(Resource):
    """Resource for creating downloads"""

    @download_api.response(413, "Allowed payload size is 1024 bytes")
    @download_api.response(400, "Download validation error")
    @download_api.response(202, "Download accepted for submission")
    @download_api.expect(download, validate=True)
    def post(self):
        download_data = download_api.payload
        if download_data["name"]:
            try:
                task = celery.send_task(
                    "tasks.chart_download", args=[download_api.payload]
                )
                logger.info("Helm chart download start task %s", task.id)
            except CeleryError:
                logger.critical(
                    "Logging start task failed due to celery error", exc_info=True
                )

                return (
                    {"status": "error", "message": "Unable to start download task"},
                    500,
                )
        return {
            "status": "success",
            "message": "Download {} as task {}".format(download_data["name"], task.id),
        }
