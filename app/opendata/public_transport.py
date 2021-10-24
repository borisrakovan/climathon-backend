
import os
from typing import List
import numpy as np
from app import app
import pandas as pd
from app.factor import BaseFactor

from scipy.ndimage.morphology import distance_transform_edt

from app.utils import minmax_normalize, show_heatmap


class PublicTransportFactor(BaseFactor):
    def __init__(self):
        path = os.path.join(app.config["DATA_DIR"], "mhd_aut_processed.pickle")
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

        automats = np.zeros((y_dim, x_dim))
        for idx, row in df.iterrows():
            x, y = to_coords(row["lat"], row["long"])
            automats[y_dim - y - 1, x] = 1.

        index = distance_transform_edt(1 - automats)

        index = minmax_normalize(index, min=0, max=50)
        index = np.clip(index, 0, 1)

        # show_heatmap(index)
        return 1. - index


#
# if __name__ == "__main__":
#     f = PublicTransportFactor()
#     f.get_index_layer(
#         bounds=[17.006149, 48.087483, 17.227249, 48.21598],
#         size=[500, 500])
#     return