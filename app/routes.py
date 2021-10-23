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

    index = np.random.rand(80, 120)

    return {
        "result": {
            "index": get_thermal_data(coords_bbox=data["bounds"]).tolist()
        }
    }
