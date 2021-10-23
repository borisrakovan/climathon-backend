import numpy as np
from flask import request, Response
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

    index = np.random.rand(80, 120)

    return {
        "result": {
            "bounds": data["bounds"],
            "size": data['size'],
            "index": get_thermal_data(coords_bbox=data["bounds"], bounds_size=data['size'])
        }
    }


@app.route("/factors", methods=["GET"])
def factors():
    return [
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