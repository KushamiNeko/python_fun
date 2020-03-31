from typing import List, Optional

# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.plotter.plotter import TextPlotter
from fun.trading.transaction import FuturesTransaction


class LeverageRecords(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        records: List[FuturesTransaction],
        offset: float = 0.0025,
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

        loc = []
        for r in self._records:
            where = np.argwhere(dates == r.datetime()).flatten()
            if where.size != 0:
                loc.append(where.min())

        loc = np.array(loc)

        unique, count = np.unique(loc, return_counts=True)
        labels = np.where(
            ops == 0,
            "X",
            np.vectorize(lambda v: f"{v[0].strip()}\n{v[1:].strip()}")(
                np.vectorize(lambda v: f"L{v:.0f}" if v > 0 else f"S{v:.0f}")(ops)
            ),
        )

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]
        middle = (highs.max() + lows.min()) / 2.0

        # if ax is None:
        #     ax = plt.gca()

        for i, x in enumerate(unique):
            h = highs.iloc[x]
            l = lows.iloc[x]
            m = (h + l) / 2.0

            y = l * (1 - self._offset) if m > middle else h * (1 + self._offset)
            va = "top" if m > middle else "bottom"

            text = "".join([labels[j] for j in np.argwhere(loc == x).flatten()])

            ax.text(
                x,
                y,
                text,
                color=self._font_color,
                fontproperties=self._font_properties,
                ha="center",
                va=va,
            )
