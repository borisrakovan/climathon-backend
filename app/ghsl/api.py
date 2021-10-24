import json
from typing import List

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.mask
from fiona.crs import from_epsg
from rasterio.plot import show
from scipy.interpolate import RegularGridInterpolator
from shapely.geometry import box

from app.factor import BaseFactor


class GhslFactor(BaseFactor):

    TIF_PATH = '../data/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0.tif'

    @staticmethod
    def get_features(gdf):
        """
        Function to parse features from GeoDataFrame in such a manner that rasterio wants them.
        """
        return [json.loads(gdf.to_json())['features'][0]['geometry']]

    def get_index_layer(self, bounds: List[float], size: List[int]) -> np.ndarray:
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

            return out_image


if __name__ == '__main__':
    show(GhslFactor().get_index_layer(
        bounds=[16.941540682073867, 48.08774893052057, 17.241277652978773, 48.247859693476855],
        size=[1000, 1000])
    )