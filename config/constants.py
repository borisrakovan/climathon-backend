import os
from pathlib import Path
from sentinelhub import SHConfig
from singleton_decorator import singleton

from config import loader


@singleton
class Constants:
    def __init__(self):

        # --------------- Sentinelhub --------------------
        self.SENTINELHUB_CLIENT_ID = loader.get('sentinelhub', 'client_id')
        self.SENTINELHUB_CLIENT_SECRET = loader.get('sentinelhub', 'client_secret')
        self.SENTINELHUB_INSTANCE_ID = loader.get('sentinelhub', 'instance_id')

        self.SENTINEL_HUB_AUTH_CONFIG = SHConfig()
        self.SENTINEL_HUB_AUTH_CONFIG.instance_id = self.SENTINELHUB_INSTANCE_ID
        self.SENTINEL_HUB_AUTH_CONFIG.sh_client_id = self.SENTINELHUB_CLIENT_ID
        self.SENTINEL_HUB_AUTH_CONFIG.sh_client_secret = self.SENTINELHUB_CLIENT_SECRET
        self.SENTINEL_HUB_AUTH_CONFIG.save()
