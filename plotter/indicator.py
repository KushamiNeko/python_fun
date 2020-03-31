from datetime import datetime
from typing import Optional, List, Union
from abc import ABCMeta, abstractmethod

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

            # if self._slice_start is not None and self._slice_end is not None:
            # ys = ys.loc[self._slice_start : self._slice_end]

            # ax.plot(
            # xs,
            # ys,
            # color=self._line_color,
            # alpha=self._line_alpha,
            # linewidth=self._line_width,
            # )


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
        assert quotes is not None

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

    # simple_moving_average(self._extended_quotes.loc[:, "close"], 5).loc[s:e],


class BollinggerBand(Indicator):
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
        assert quotes is not None

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


# def relative_strength(df: pd.DataFrame, rdf: pd.DataFrame,) -> pd.DataFrame:
# return df / rdf
