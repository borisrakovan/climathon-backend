import numpy as np
from flask import request, Response
from .satelites.api import get_thermal_data, get_ndvi_index
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


@app.route("/ndvi")
def ndvi_test():
    return {
        "result": {
            "index": get_ndvi_index()
        }
    }


@app.route("/index", methods=["POST"])
def index():
    data = request.get_json(force=True)

    return {
        "result": {
            "bounds": data["bounds"],
            "size": data['size'],
            "index": get_thermal_data(coords_bbox=data["bounds"], bounds_size=data['size'])
        }
    }
