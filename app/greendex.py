import numpy as np
from collections import namedtuple
from typing import List

from .opendata.pollution import PollutionFactor
from .opendata.public_transport import PublicTransportFactor
from .satelites.api import HeatFactor, VegetationFactor
from .ghsl.api import GhslFactor

FactorTuple = namedtuple("FactorTuple", "id,name,cls")
F = FactorTuple

all_factors = [
    F("1", "Heat islands", HeatFactor),
    F("2", "Sources of pollution", PollutionFactor),
    F("3", "Vegetation", VegetationFactor),
    F("4", "Human settlements density", GhslFactor),
    F("5", "Public transport availability", PublicTransportFactor),
]


class Greendex:
    @staticmethod
    def compute(factors: List[FactorTuple], weights: List[float],
                bounds: List[float], size: List[float]) -> np.ndarray:
        num_factors = len(factors)
        index_layers = np.zeros((num_factors, size[0], size[1]))

        for i, factor_tuple in enumerate(factors):
            factor_instance = factor_tuple.cls()
            index_layers[i, ...] = factor_instance.get_index_layer(bounds, size)

        final_index = np.average(index_layers, axis=0, weights=weights)

        return final_index