from datetime import timedelta
from typing import List, Optional

import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.data.source import FREQUENCY, WEEKLY
from fun.plotter.plotter import TextPlotter
from fun.trading.transaction import FuturesTransaction


class LeverageRecords(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        records: List[FuturesTransaction],
        offset: float = 0.001,
        font_color: str = "k",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._quotes = quotes
        self._frequency = frequency

        self._records = records

        self._offset = offset

    def plot(self, ax: axes.Axes) -> None:
        if len(self._quotes) == 0 or len(self._records) == 0:
            return

        assert ax is not None

        dates = self._quotes.index
        ops = np.add.accumulate(
            [float(f"{r.operation()}{r.leverage()}") for r in self._records]
        )

        ops_s = -1
        ops_e = -1

        loc = []
        for i, r in enumerate(self._records):
            tar = r.datetime()
            if ops_s == -1 and tar >= dates[0]:
                ops_s = i
            if ops_e == -1 and tar > dates[-1]:
                ops_e = i

            if self._frequency == WEEKLY:
                tar = tar - timedelta(days=tar.weekday())

            where = np.argwhere(dates == tar).flatten()
            if where.size != 0:
                loc.append(where.min())

        assert ops_s != -1
        if ops_e == -1:
            ops_e = len(self._records)

        ops = ops[ops_s:ops_e]

        loc = np.array(loc)

        unique, count = np.unique(loc, return_counts=True)
        labels = np.where(
            ops == 0,
            "X",
            np.vectorize(lambda v: f"{v[0].strip()}\n{v[1:].strip()}")(
                np.vectorize(lambda v: f"L{abs(v):.0f}" if v > 0 else f"S{abs(v):.0f}")(
                    ops
                )
            ),
        )

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]
        middle = (highs.max() + lows.min()) / 2.0

        for x in unique:
            h = highs.iloc[x]
            l = lows.iloc[x]
            m = (h + l) / 2.0

            y = l * (1 - self._offset) if m > middle else h * (1 + self._offset)
            va = "top" if m > middle else "bottom"

            text = "\n".join([labels[j] for j in np.argwhere(loc == x).flatten()])

            ax.text(
                x,
                y,
                text,
                color=self._font_color,
                fontproperties=self._font_properties,
                ha="center",
                va=va,
            )
