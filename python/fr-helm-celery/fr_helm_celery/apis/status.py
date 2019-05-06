""" Returns job task status json payload - including message from helm API
"""

import celery.states as states
from flask_restplus import Namespace, Resource

from fr_helm_celery.helm import celery


status_api = Namespace(
    "status", description="Service asynchronous task status information"
)


@status_api.route("/<string:task_id>")
@status_api.response(201, "Celery task finished sucessfully")
@status_api.response(202, "Celery task is being processed")
@status_api.response(404, "No task found for task id")
@status_api.response(409, "Celery task returned a failed status / conflict error")
class CeleryCheckTask(Resource):
    def get(self, task_id):
        """Returns status json from celery task_id
        """
        res = celery.AsyncResult(task_id)
        if not res:
            return "", 404
        body = {"id": task_id}
        if res.result:
            body["result"] = str(res.result)
        body["status"] = str(res.state)
        if res.state in (states.STARTED, states.RECEIVED, states.PENDING, states.RETRY):
            return body, 202
        elif res.state in (states.SUCCESS, states.FAILURE, states.REVOKED):
            return body, 201
        else:
            return {"status": "{}".format(res.state)}, 409
