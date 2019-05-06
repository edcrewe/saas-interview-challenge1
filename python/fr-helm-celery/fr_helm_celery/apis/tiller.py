"""Helm Charts
"""
import logging
from fr_helm_celery.helm import celery

from flask_restplus import Resource, Namespace, fields
from celery.exceptions import CeleryError

logger = logging.getLogger()

tiller_api = Namespace("tiller", description="Tiller releases data")

tiller = tiller_api.model(
    "TillerMetadata",
    {
        "host": fields.String(required=True, description="Tiller host"),
        "port": fields.Integer(required=True, description="Tiller port", default=44134),
        "tls": fields.String(
            required=False, description="Tiller TLS config", default=""
        ),
        "namespace": fields.String(
            required=False, description="Filter releases by namespace", default=""
        ),
        "status_codes": fields.String(
            required=False, description="Filter releases by status", default=""
        ),
    },
)


@tiller_api.route("/")
class Tiller(Resource):
    """Resource for listing or modifying releases"""

    @tiller_api.response(413, "Allowed payload size is 1024 bytes")
    @tiller_api.response(400, "Tiller validation error")
    @tiller_api.response(202, "Tiller accepted for submission")
    @tiller_api.expect(tiller, validate=True)
    def post(self):
        tiller_data = tiller_api.payload
        try:
            task = celery.send_task("tasks.tiller_list", args=[tiller_api.payload])
            logger.info("Helm list releases start task %s", task.id)
        except CeleryError:
            logger.critical(
                "Logging start task failed due to celery error", exc_info=True
            )

            return (
                {"status": "error", "message": "Unable to start tiller list releases"},
                500,
            )
        return {
            "status": "success",
            "message": "Tiller list releases for {} as task {}".format(
                tiller_data["namespace"], task.id
            ),
        }
