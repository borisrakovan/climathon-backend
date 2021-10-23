import numpy as np
from flask import request, Response

from .opendata.pollution import PollutionFactor
from .satelites.api import get_thermal_data
from app import app


@app.route('/', methods=["GET"])
def test():
    return f'Hi! Debug: {app.config["DEBUG"]}'


@app.route("/thermal")
def thermal_test():
    return {
        "result": {
            "index": get_thermal_data()
        }
    }


@app.route("/index", methods=["POST"])
def index():
    data = request.get_json(force=True)

    thermal_index = get_thermal_data(coords_bbox=data["bounds"], bounds_size=data['size'])
    pollution_index = PollutionFactor()
    return {
        "result": {
            "bounds": data["bounds"],
            "size": data['size'],
            "index": pollution_index.get_index_values(data["bounds"], data["size"]),
        }
    }


@app.route("/factors", methods=["GET"])
def factors():
    return {
        "result": [
            {
                "id": 1,
                "name": "Heat islands",
            },
            {
                "id": 2,
                "name": "Air pollution",
            },
            {
                "id": 3,
                "name": "Precipitation",
            },
        ]
    }