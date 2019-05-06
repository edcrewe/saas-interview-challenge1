"""Integration tests for telemetry task"""
import os
import json
import unittest
import time

from fr_helm_celery.helm.tasks import chart_download
from fr_helm_celery.app import app


class TestRestTask(unittest.TestCase):
    """Test Celery run of the download chart task
       This task takes the JSON payload and sends it to chart_download task.
       It tests it both directly as a task and via the test web client and REST API
    """

    payload = {
        "name": "mongodb",
        "source_location": "https://kubernetes-charts.storage.googleapis.com/",
    }
    client = None

    @classmethod
    def setUpClass(cls):
        """Run fixture log process_log_json task via celery once for all tests"""
        cls.task = chart_download.apply_async(args=[cls.payload])
        cls.response = cls.task.get()
        cls.client = app.test_client()

    def test_task_state(self):
        self.assertEqual(self.task.state, "SUCCESS")

    def test_yaml(self, response=None):
        """Check task retrieves yaml"""
        if not response:
            response = self.response
        self.assertIn("NoSQL document-oriented database", response["yaml"])

    def test_client_post(self):
        """Check that web post returns task id then wait until it returns completed task
           and rerun test_yaml on its result"""
        rv = self.client.post(
            "/v1/download/",
            data=json.dumps(self.payload),
            content_type="application/json",
            follow_redirects=True,
        )
        self.assertTrue(
            rv.data,
            "No data returned from Chart download data post, status {}".format(
                rv.status
            ),
        )
        self.assertEqual(
            "202 ACCEPTED",
            rv.status,
            "Failed to create Chart download task: {}".format(rv.data),
        )
        self.assertTrue(rv.data)
        task = rv.json
        self.assertIn("task_id", task.keys())
        task_url = "/v1/task/{}".format(task["task_id"])
        response = None
        for sec in range(0, 3):
            time.sleep(sec + 0.2)
            rv = self.client.get(
                task_url, content_type="application/json", follow_redirects=True
            )
            self.assertTrue(int(rv.status_code) in [200, 201, 202, 203])
            if rv.is_json and "201 CREATED" == rv.status:
                response = rv.json
                break
        self.test_yaml(response)
