from abc import abstractmethod
from datetime import datetime
from typing import List, NewType, Optional, Union

import numpy as np
import pandas as pd
from matplotlib import axes

from fun.plotter.plotter import LinePlotter


class Indicator(LinePlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        slice_start: Optional[datetime] = None,
        slice_end: Optional[datetime] = None,
        line_color: str = "k",
        line_alpha: float = 1.0,
        line_width: float = 10.0,
    ) -> None:
        assert quotes is not None

        super().__init__(
            line_color=line_color, line_alpha=line_alpha, line_width=line_width,
        )

        self._quotes = quotes
        self._slice_start = slice_start
        self._slice_end = slice_end

    @abstractmethod
    def _calculate(self) -> Union[pd.Series, List[pd.Series]]:
        raise NotImplementedError

    def _render(self, ax: axes.Axes, ys: pd.DataFrame) -> None:
        if self._slice_start is not None and self._slice_end is not None:
            ys = ys.loc[self._slice_start : self._slice_end]

        ax.plot(
            np.arange(len(ys)),
            ys,
            color=self._line_color,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )

    def plot(self, ax: axes.Axes) -> None:

        calc = self._calculate()

        assert type(calc) in (list, pd.Series)

        if type(calc) == list:
            for ys in calc:
                self._render(ax, ys)
        elif type(calc) == pd.Series:
            self._render(ax, calc)
        else:
            raise ValueError("invalid return type from calculate")


class SimpleMovingAverage(Indicator):
    def __init__(
        self,
        n: int,
        quotes: pd.DataFrame,
        slice_start: Optional[datetime] = None,
        slice_end: Optional[datetime] = None,
        line_color: str = "k",
        line_alpha: float = 1.0,
        line_width: float = 10.0,
    ) -> None:

        super().__init__(
            quotes=quotes,
            slice_start=slice_start,
            slice_end=slice_end,
            line_color=line_color,
            line_alpha=line_alpha,
            line_width=line_width,
        )

        self._n = n

    def _calculate(self) -> pd.Series:
        return self._quotes.loc[:, "close"].rolling(self._n).mean()


class BollingerBand(Indicator):
    def __init__(
        self,
        n: int,
        m: float,
        quotes: pd.DataFrame,
        slice_start: Optional[datetime] = None,
        slice_end: Optional[datetime] = None,
        line_color: str = "k",
        line_alpha: float = 1.0,
        line_width: float = 10.0,
    ) -> None:

        super().__init__(
            quotes=quotes,
            slice_start=slice_start,
            slice_end=slice_end,
            line_color=line_color,
            line_alpha=line_alpha,
            line_width=line_width,
        )

        self._n = n
        self._m = m

    def _calculate(self,) -> List[pd.DataFrame]:
        mean = self._quotes.loc[:, "close"].rolling(self._n).mean()

        return [
            mean + (self._quotes.loc[:, "close"].rolling(self._n).std() * self._m),
            mean + (self._quotes.loc[:, "close"].rolling(self._n).std() * -self._m),
        ]


class RelativeStrength(Indicator):
    def __init__(
        self,
        quotes: pd.DataFrame,
        quotes_b: pd.DataFrame,
        slice_start: Optional[datetime] = None,
        slice_end: Optional[datetime] = None,
        line_color: str = "k",
        line_alpha: float = 1.0,
        line_width: float = 10.0,
    ) -> None:

        super().__init__(
            quotes=quotes,
            slice_start=slice_start,
            slice_end=slice_end,
            line_color=line_color,
            line_alpha=line_alpha,
            line_width=line_width,
        )

        self._quotes_b = quotes_b

    def _calculate(self,) -> pd.Series:
        a = self._quotes.loc[:, "close"]
        b = self._quotes_b.loc[:, "close"]

        return a / b


RANGE_SRC = NewType("RANGE_SRC", int)
BODY_RANGE = RANGE_SRC(0)
SHADOW_RANGE = RANGE_SRC(1)


class CandleRange(Indicator):
    def __init__(
        self,
        quotes: pd.DataFrame,
        moving_average: int = 0,
        range_type: RANGE_SRC = BODY_RANGE,
        slice_start: Optional[datetime] = None,
        slice_end: Optional[datetime] = None,
        line_color: str = "k",
        line_alpha: float = 1.0,
        line_width: float = 10.0,
    ) -> None:

        super().__init__(
            quotes=quotes,
            slice_start=slice_start,
            slice_end=slice_end,
            line_color=line_color,
            line_alpha=line_alpha,
            line_width=line_width,
        )

        assert moving_average >= 0
        assert range_type in (BODY_RANGE, SHADOW_RANGE)

        self._moving_average = moving_average
        self._range_type = range_type

    def _calculate(self,) -> pd.Series:
        height: pd.Series

        if self._range_type == BODY_RANGE:
            height = self._quotes.loc[:, "open"] - self._quotes.loc[:, "close"]
            height = height.abs()

        elif self._range_type == SHADOW_RANGE:
            height = self._quotes.loc[:, "high"] - self._quotes.loc[:, "low"]

        else:
            raise ValueError("invalid range type")

        if self._moving_average != 0:
            height = height.rolling(self._moving_average).mean()

        return height
