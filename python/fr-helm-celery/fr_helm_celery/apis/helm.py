"""Helm Charts
"""
import logging

from flask_restplus import Resource, Namespace, Model, fields
from pyhelm.chartbuilder import ChartBuilder

logger = logging.getLogger()

chart_api = Namespace("chart", description="Send charts")

chart = Model(
    "ChartMetadata",
    {
        "name": fields.String(required=True, description="Service name"),
        "version": fields.String(required=True, description="Service version"),
        "source_type": fields.String(required=True, description="Chart source type"),
        "source_location": fields.String(
            required=True, description="Chart source type"
        ),
    },
)


@chart_api.route("/")
class Chart(Resource):
    """Resource for creating charts"""

    @chart_api.response(413, "Allowed telemetry payload size is 1024 bytes")
    @chart_api.response(400, "Chart validation error")
    @chart_api.response(202, "Chart accepted for submission")
    @chart_api.expect(chart, validate=True)
    def post(self):
        chart_data = chart_api.payload
        chart = ChartBuilder(
            {
                "name": chart_data["name"],
                "source": {
                    "type": chart_data["source_type"],
                    "location": chart_data["source_location"],
                },
            }
        )
        if chart:
            return "Got chart"
