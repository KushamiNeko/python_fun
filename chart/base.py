import io
from abc import ABCMeta, abstractmethod
from typing import List, NewType, Optional, Tuple, Union

import numpy as np
import pandas as pd

from fun.plotter.plotter import Plotter

CHART_SIZE = NewType("CHART_SIZE", int)
LARGE_CHART = CHART_SIZE(0)
MEDIUM_CHART = CHART_SIZE(1)
SMALL_CHART = CHART_SIZE(2)


class ChartFactory(metaclass=ABCMeta):
    def __init__(self, quotes: pd.DataFrame,) -> None:
        assert quotes is not None

        self._quotes = quotes

    def quotes_range(self) -> Tuple[float, float]:
        mn = np.amin(self._quotes.loc[:, "low"])
        mx = np.amax(self._quotes.loc[:, "high"])

        return mn, mx

    def chart_xrange(self) -> Tuple[float, float]:
        return -0.5, (len(self._quotes) - 1) + 0.5

    def chart_yrange(self) -> Tuple[float, float]:
        extend_ratio = 25.0

        mn, mx = self.quotes_range()
        r = mx - mn

        return (
            mn - (r / extend_ratio),
            mx + (r / extend_ratio),
        )

    @abstractmethod
    def to_data_coordinates(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        raise NotImplementedError

    @abstractmethod
    def render(
        self,
        output: Optional[Union[str, io.BytesIO]] = None,
        plotters: Optional[List[Plotter]] = None,
        interactive: bool = False,
    ) -> None:
        raise NotImplementedError


class CandleSticks(ChartFactory):
    def _minimum_height(self) -> float:
        # ratio = 0.00025
        ratio = 0.001
        mn, mx = self.quotes_range()
        r = mx - mn

        return r * ratio
