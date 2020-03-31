from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.plotter.plotter import Plotter
from fun.trading.transaction import FuturesTransaction


class LeverageRecords(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        records: List[FuturesTransaction],
        offset: float = 0.01,
        color: str = "k",
        font_size: float = 10.0,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        self._quotes = quotes
        self._records = records

        self._offset = offset

        self._color = color

        if font_properties is None:
            self._font_properties = fm.FontProperties(size=font_size)
        else:
            self._font_properties = font_properties

    def plot(self, ax: axes.Axes) -> None:
        if len(self._quotes) == 0 or len(self._records) == 0:
            return

        dates = self._quotes.index
        ops = np.add.accumulate(
            [float(f"{r.operation()}{r.leverage()}") for r in self._records]
        )
        loc = np.array(
            [np.argwhere(dates == r.datetime()).min() for r in self._records]
        )

        unique, count = np.unique(loc, return_counts=True)
        labels = np.where(ops == 0, "X", np.vectorize(lambda v: f"{v:+.0f}")(ops))

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]
        middle = (highs.max() + lows.min()) / 2.0

        if ax is None:
            ax = plt.gca()

        for i, x in enumerate(unique):
            h = highs.iloc[x]
            l = lows.iloc[x]
            m = (h + l) / 2.0

            y = l * (1 - self._offset) if m > middle else h * (1 + self._offset)
            va = "top" if m > middle else "bottom"
            rt = 90 if m > middle else -90

            text = "".join([labels[j] for j in np.argwhere(loc == x).flatten()])

            ax.text(
                x,
                y,
                text,
                color=self._color,
                fontproperties=self._font_properties,
                ha="left",
                va=va,
                rotation=rt,
            )
