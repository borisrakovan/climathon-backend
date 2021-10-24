from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BaseFactor:

    @abstractmethod
    def get_index_layer(self, bounds: List[float], size: List[float]) -> np.ndarray:
        pass
