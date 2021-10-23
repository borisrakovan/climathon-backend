import os
import math
import numpy as np

from typing import List
import pandas as pd
# import matplotlib.pyplot as plt

from app.factor import BaseFactor
from app import app


class PollutionFactor(BaseFactor):
    def __init__(self):
        path = os.path.join(app.config["DATA_DIR"], "zdroje_znecistenia_processed.pickle")
        self.df = pd.read_pickle(path)

    def get_index_values(self, bounds: List[float], size: List[float]) -> List[List[float]]:
        lng1, lat1, lng2, lat2 = bounds
        y_dim, x_dim = size
        print(bounds)
        print(size)
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

        # r = int(y_dim * (radius_lat / (lat2 - lat1)))

        # index_temp = np.zeros((y_dim + 2 * r, x_dim + 2 * r), dtype=np.float32)
        index = np.zeros((y_dim, x_dim))

        for idx, row in df.iterrows():
            x, y = to_coords(row["lat"], row["long"])
            index[y, x] = 1
            # x_mid = x + r
            # y_mid = y + r
            # y_frm, y_to = max(0, y-r), min(y_dim-1, y+r)
            # x_frm, x_to = max(0, x-r), min(x_dim-1, x+r)
            # index_temp[(y_mid - r):(y_mid + r + 1), (x_mid - r):(x_mid + r + 1)] \
            #     += self.gkern(l=r * 2 + 1)
            # index_temp[y_mid, x_mid] += 1

        # index = index_temp[r:y_dim + r, r:x_dim + r]
        # print(index_temp.shape)
        print(index.shape)
        print(index[index != 0].shape)
        #
        # def hmap(arr):
        #     plt.imshow(arr, cmap='hot', interpolation='nearest')
        #     plt.show()

        return index.tolist()

    @staticmethod
    def gkern(l, sig=1.):
        """\
        creates gaussian kernel with side length `l` and a sigma of `sig`
        """
        ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
        gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
        kernel = np.outer(gauss, gauss)
        return kernel / np.sum(kernel)

    @staticmethod
    def meters_to_lat(ms):
        return ms / 111111

    @staticmethod
    def meters_to_lng(ms, lat):
        return ms / (111111 * math.cos(lat))


# if __name__ == "__main__":
#     PollutionFactor()