import numpy as np
from flask import request, Response
from .satelites.api import get_thermal_data
from app import app


@app.route('/', methods=["GET"])
def test():
    return f'Hi! Debug: {app.config["DEBUG"]}'


@app.route("/index", methods=["POST"])
def index():
    data = request.get_json(force=True)

    if "fromCoord" not in data:
        return "Missing parameter: fromCoord", 400

    if "toCoord" not in data:
        return "Missing parameter: toCoord", 400

    return {
        "result": {
            "fromCoord": data["fromCoord"],
            "toCoord": data["toCoord"],
            "index": get_thermal_data(coords_bbox=data["bounds"])
        }
    }