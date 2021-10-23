
from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest, WmsRequest
import numpy as np
import logging
from typing import List, Optional
from config import constants


def get_thermal_data(coords_bbox: Optional[List] = [17.006149, 48.087483, 17.227249, 48.21598],
                     bounds_size: Optional[List] = [500, 500],
                     date_interval: Optional[List] = None):

    print(bounds_size)
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
        bbox=BBox(bbox=coords_bbox, crs=CRS.WGS84),
        size=tuple(bounds_size),
        config=constants.SENTINEL_HUB_AUTH_CONFIG
    )

    try:
        img = request_true_color.get_data()[0]

        img = ((img - 250) / 70)
        img[np.isnan(img)] = 0

        return img.tolist()

    except Exception as e:
        print(f"unable to fetch Landsat8 thermal data. {e}")
        logger.error(f"unable to fetch Landsat8 thermal data. {e}")


