from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from matplotlib import ticker

from fun.data.source import DAILY, FREQUENCY, HOURLY, MONTHLY, WEEKLY


class Ticker(metaclass=ABCMeta):
    @abstractmethod
    def ticks(self) -> Dict[float, str]:
        raise NotImplementedError


class TimeTicker(Ticker):
    def __init__(self, quotes: pd.DataFrame) -> None:
        self._quotes = quotes

    def ticks(self) -> Dict[float, str]:
        frequency: FREQUENCY

        start = self._quotes.index[0]
        end = self._quotes.index[-1]

        period = end - start
        if period.days < 30:
            frequency = HOURLY
        elif period.days < 365 * 2:
            frequency = DAILY
        elif period.days < 365 * 7:
            frequency = WEEKLY
        else:
            frequency = MONTHLY

        assert frequency is not None

        loc: List[int] = []
        labels: List[str] = []

        if frequency == DAILY:
            dates = self._quotes.index.strftime("%Y-%b")
            labels = np.unique(dates)
            loc = [np.argwhere(dates == l).min() for l in labels]

        elif frequency == WEEKLY:
            dates = self._quotes.index.strftime("%Y-%b")
            labels = np.unique(dates)
            loc = [np.argwhere(dates == l).min() for l in labels]

            func = np.vectorize(
                lambda x: x.split("-")[0] if "Jan" in x else x.split("-")[1]
            )
            labels = func(labels)

        elif frequency == MONTHLY:
            dates = self._quotes.index.strftime("%Y")
            labels = np.unique(dates)
            loc = [np.argwhere(dates == l).min() for l in labels]

        return {k: v for k, v in zip(loc, labels)}


class StepTicker(Ticker):
    def __init__(
        self,
        mn: float,
        mx: float,
        nbins: int = 25,
        steps: Optional[List[int]] = [1, 2, 5, 10],
        decimals: int = 2,
    ) -> None:

        self._nbins = nbins
        self._steps = steps
        self._min = mn
        self._max = mx

        self._decimals = decimals

    def ticks(self) -> Dict[float, str]:
        locator = ticker.MaxNLocator(nbins=self._nbins, steps=self._steps)
        values = locator.tick_values(self._min, self._max)

        return {v: f"{v:.{self._decimals}f}" for v in values}
