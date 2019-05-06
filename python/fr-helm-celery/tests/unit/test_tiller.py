#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test that the tiller task works"""

from unittest import TestCase
from unittest import mock
from pyhelm import tiller
from supermutes.dot import dotify
from fr_helm_celery.helm.tasks import tiller_list

releases = [
    {
        "name": "plucking-leopard",
        "revision": 1,
        "updated": "Mon May  6 08:56:56 2019",
        "status": "DEPLOYED",
        "chart": "cmp-platform-6.5.1",
        "namespace": "default",
    }
]


class TestTillerList(TestCase):
    """Test the tiller_list task via mocking underlying pyhelm methods"""

    payload = {
        "host": "localhost",
        "port": 44134,
        "namespace": "default",
        "status_codes": "",
    }

    def setUp(self):
        """Test set up"""
        pass

    @mock.patch("pyhelm.tiller.ReleaseServiceStub")
    @mock.patch("pyhelm.tiller.ListReleasesRequest")
    def test_list_releases(self, mock_list_release_request, mock_release_service_stub):
        """Call the tiller_list task directly rather than as asynch since we are mocking
           the pyhelm methods it should call to make it a unit test"""
        mock_release_service_stub.return_value.ListReleases.return_value = [
            dotify({"next": "", "releases": releases})
        ]
        result = tiller_list(self.payload)
        mock_list_release_request.assert_called_with(
            limit=tiller.RELEASE_LIMIT,
            offset=None,
            namespace="default",
            status_codes=[],
        )
        mock_release_service_stub.return_value.ListReleases.assert_called()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["chart"], "cmp-platform-6.5.1")
