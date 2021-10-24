
import numpy as np
from flask import request, Response
from .opendata.pollution import PollutionFactor

from app import app
from .greendex import all_factors, Greendex
from .satelites.api import HeatFactor, VegetationFactor


@app.route('/', methods=["GET"])
def test():
    return f'Hi! Debug: {app.config["DEBUG"]}'


@app.route("/thermal")
def thermal_test():
    factor = HeatFactor()
    return {
        "result": {
            "index": factor.get_index_layer(
                bounds=[17.006149, 48.087483, 17.227249, 48.21598],
                size=[500, 500])
        }
    }


@app.route("/ndvi")
def ndvi_test():
    factor = VegetationFactor()
    return {
        "result": {
            "index": factor.get_index_layer(
                bounds=[17.006149, 48.087483, 17.227249, 48.21598],
                size=[500, 500])
        }
    }


@app.route("/index", methods=["POST"])
def index():
    data = request.get_json(force=True)

    size = data["size"]
    bounds = data["bounds"]
    input_factors = data.get("factorWeights")
    print(input_factors)
    if input_factors is None or len(input_factors) == 0 or sum(input_factors.values()) == 0.:
        factors = all_factors
        weights = [1] * len(factors)
    else:
        factors = [f for f in all_factors if f.id in input_factors.keys()]
        weights = [input_factors[f.id] for f in factors]

    index = Greendex.compute(factors, weights, bounds, size)

    return {
        "result": {
            "bounds": bounds,
            "size": size,
            "index": index.tolist()
        }
    }


@app.route("/factors", methods=["GET"])
def factors():
    return {
        "result": [
            {
                "id": f.id,
                "name": f.name,
            }
            for f in all_factors
        ]
    }