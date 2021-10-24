from collections import namedtuple

import numpy as np
from flask import request, Response
from .satelites.api import get_thermal_data, get_ndvi_index
from .opendata.pollution import PollutionFactor
from app import app


FactorTuple = namedtuple("FactorTuple", "id,name,cls")
F = FactorTuple

all_factors = [
    F("1", "Heat islands", None),
    F("2", "Air pollution", PollutionFactor),
]

def get_factor(id):
    return next((f for f in all_factors if f.id == str(id)))


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

    thermal_index = get_thermal_data(coords_bbox=data["bounds"], bounds_size=data['size'])

    size = data["size"]
    bounds = data["bounds"]
    factor_weights = data["factorWeights"]

    num_factors = len(all_factors)
    index_values = np.zeros((num_factors, size[0], size[1]))

    # for i, factor_tuple in enumerate(all_factors):
    #     factor = factor_tuple.cls()
    #     index_values[i, ...] = factor.get_index_values(bounds, size)

    # weights =
    # final_index = np.average(index_values, axis=0, weights=0)
    pollution_index = PollutionFactor()

    return {
        "result": {
            "bounds": data["bounds"],
            "size": size,
            "index": pollution_index.get_index_values(bounds, size),
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