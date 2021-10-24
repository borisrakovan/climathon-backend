from abc import ABC, abstractmethod
from typing import List


class BaseFactor:

    @abstractmethod
    def get_index_values(self, bounds: List[float], size: List[float]) -> List[List[float]]:
        pass
