import numpy as np
from flask import request, Response

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

    index = np.random.rand(16, 20)
    return {
        "result": {
            "fromCoord": data["fromCoord"],
            "toCoord": data["toCoord"],
            "index": index.tolist()
        }
    }