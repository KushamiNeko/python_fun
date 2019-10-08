import re
from typing import Tuple

import numpy as np
import pandas as pd


class Chart:
    def __init__(self, quotes: pd.DataFrame, chart_size: str = "l"):

        assert quotes is not None
        assert re.match(r"^m|l$", chart_size.lower())

        self._quotes = quotes
        self._chart_size = chart_size.lower()

    @property
    def _body_min_height(self) -> float:
        mn, mx = self._ylim_from_price_range()
        r = mx - mn

        # return r * 0.001
        return r * 0.002

    @property
    def _price_range_extend_ratio(self) -> float:
        return 25.0

    def _ylim_from_price_range(self) -> Tuple[float, float]:
        mn = np.amin(self._quotes["low"].to_numpy())
        mx = np.amax(self._quotes["high"].to_numpy())

        r = mx - mn

        return (
            mn - (r / self._price_range_extend_ratio),
            mx + (r / self._price_range_extend_ratio),
        )

    def _calculate_candlesticks_body_top_bottom(self) -> Tuple[np.array, np.array]:
        dec = self._quotes["open"] > self._quotes["close"]

        r = np.abs(self._quotes["open"] - self._quotes["close"])
        avg = (self._quotes["open"] + self._quotes["close"]) / 2.0

        mini = r < self._body_min_height

        top = np.copy(self._quotes["close"].to_numpy())
        bottom = np.copy(self._quotes["open"].to_numpy())

        top[dec] = self._quotes[dec]["open"].to_numpy()
        bottom[dec] = self._quotes[dec]["close"].to_numpy()

        top[mini] = avg[mini].to_numpy() + (self._body_min_height / 2.0)
        bottom[mini] = avg[mini].to_numpy() - (self._body_min_height / 2.0)

        return (top, bottom)
