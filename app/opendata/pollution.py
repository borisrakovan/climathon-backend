import os
import math
import numpy as np

from typing import List
import pandas as pd

from app.factor import BaseFactor
from app import app
from app.utils import gaussian_kernel, minmax_normalize


class PollutionFactor(BaseFactor):
    def __init__(self):
        path = os.path.join(app.config["DATA_DIR"], "zdroje_znecistenia_processed.pickle")
        self.df = pd.read_pickle(path)

    def get_index_layer(self, bounds: List[float], size: List[float]) -> np.ndarray:
        lng1, lat1, lng2, lat2 = bounds
        y_dim, x_dim = size

        def is_valid_coords(lat, lng):
            return lat1 < lat < lat2 and lng1 < lng < lng2

        def to_coords(lat, lng):
            y = y_dim * ((lat - lat1) / (lat2 - lat1))
            x = x_dim * ((lng - lng1) / (lng2 - lng1))

            return int(x), int(y)

        df = self.df[self.df.apply(lambda row: is_valid_coords(row["lat"], row["long"]), axis=1)]
        # print(df["adresa"])

        # radius = 1000
        # radius_lat = self.meters_to_lat(radius)

        r = int(0.005 / ((lat2 - lat1) / y_dim))
        sigma = int(0.0008 / ((lat2 - lat1) / y_dim))
        # print(f"r = {r}")
        # print(f"o = {sigma}")
        # r = int(y_dim * (radius_lat / (lat2 - lat1)))

        index_temp = np.zeros((y_dim + 2 * r, x_dim + 2 * r), dtype=np.float32)
        # index = np.zeros((y_dim, x_dim))

        for idx, row in df.iterrows():
            x, y = to_coords(row["lat"], row["long"])
            # index[y_dim - y - 1, x] = 1
            x_mid = x + r
            y_mid = y_dim - y - 1 + r
            # y_frm, y_to = max(0, y-r), min(y_dim-1, y+r)
            # x_frm, x_to = max(0, x-r), min(x_dim-1, x+r)
            # print(gaussian_kernel(l=r * 2 + 1))
            index_temp[(y_mid - r):(y_mid + r + 1), (x_mid - r):(x_mid + r + 1)] \
                += gaussian_kernel(l=r * 2 + 1, sig=sigma)
            # index_temp[y_mid, x_mid] += 1

        index = index_temp[r:y_dim + r, r:x_dim + r]
        # print(index_temp.shape)
        # print(index.shape)
        # print(index[index != 0].shape)

        normalized = minmax_normalize(index)
        return 1 - normalized


    @staticmethod
    def meters_to_lat(ms):
        return ms / 111111

    @staticmethod
    def meters_to_lng(ms, lat):
        return ms / (111111 * math.cos(lat))
