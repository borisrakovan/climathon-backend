import json
import os
from typing import List

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.mask
from fiona.crs import from_epsg
from rasterio.plot import show
from scipy.interpolate import RegularGridInterpolator
from shapely.geometry import box

from app import Config
from app.factor import BaseFactor
from app.utils import minmax_normalize



class GhslFactor(BaseFactor):

    def __init__(self):
        self.TIF_PATH = os.path.join(Config.DATA_DIR, 'GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_19_3.tif')

    @staticmethod
    def get_features(gdf):
        """
        Function to parse features from GeoDataFrame in such a manner that rasterio wants them.
        """
        return [json.loads(gdf.to_json())['features'][0]['geometry']]

    def get_index_layer(self, bounds: List[float], size: List[int]) -> np.ndarray:
        try:
            with rasterio.open(self.TIF_PATH) as data:

                geo = gpd.GeoDataFrame({
                    'geometry': box(bounds[0], bounds[1], bounds[2], bounds[3])
                }, index=[0], crs=from_epsg(4326))

                geo_bounds = geo.to_crs(crs=data.crs.data)

                data_croppped, _ = rasterio.mask.mask(
                    dataset=data,
                    shapes=geo_bounds.geometry,
                    crop=True,
                    pad=True,
                    all_touched=True
                )

                m = max(data_croppped[0].shape[0], data_croppped[0].shape[1])
                y = np.linspace(0, 1.0 / m, data_croppped[0].shape[0])
                x = np.linspace(0, 1.0 / m, data_croppped[0].shape[1])
                interpolating_function = RegularGridInterpolator((y, x), data_croppped[0])

                yv, xv = np.meshgrid(np.linspace(0, 1.0 / m, size[0]), np.linspace(0, 1.0 / m, size[1]))

                out_image = interpolating_function((xv, yv))
                out_image[out_image < 0] = 0
                out_image = minmax_normalize(out_image) * 2
                out_image = [out_image > 1.2] * (2 - out_image) + [out_image <= 1.2] * out_image
                out_image = minmax_normalize(out_image)

                return out_image
        except Exception:
            return np.zeros(shape=(1, size[0], size[1])) + 0.5


if __name__ == '__main__':
    show(GhslFactor().get_index_layer(
        bounds=[16.941540682073867, 48.08774893052057, 87.241277652978773, -148.247859693476855],
        size=[1000, 1000])
    )
