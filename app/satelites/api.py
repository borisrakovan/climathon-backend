
from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest, WmsRequest
import numpy as np
import logging
from typing import List, Optional

from app.factor import BaseFactor
from config import constants


class HeatFactor(BaseFactor):
    def get_index_layer(self, bounds: List[float], size: List[float]) -> np.ndarray:
        logger = logging.getLogger("climathon-backend")
        eval_thermal = """
            //VERSION=3
            function setup() {
                return {
                  input: [{
                    bands: [ "B10"],
                  }],
                  output: {
                    bands: 1,
                    sampleType: "FLOAT32"
                  }
                }
              }
              function evaluatePixel(samples) {
                return [samples.B10]
              }
        """
        request_true_color = SentinelHubRequest(
            evalscript=eval_thermal,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.LANDSAT_OT_L1,
                    time_interval=('2020-07-01', '2020-07-30'),
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF),
            ],
            bbox=BBox(bbox=bounds, crs=CRS.WGS84),
            size=tuple(size),
            config=constants.SENTINEL_HUB_AUTH_CONFIG
        )

        try:
            img = request_true_color.get_data()[0]

            img = ((img - 250) / 70)
            img[np.isnan(img)] = 0

            return img

        except Exception as e:
            print(f"unable to fetch Landsat8 thermal data. {e}")
            logger.error(f"unable to fetch Landsat8 thermal data. {e}")
            raise e
