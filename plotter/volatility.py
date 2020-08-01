from datetime import datetime
from typing import Optional

from fun.data.source import FREQUENCY, Yahoo, StockCharts, InvestingCom
from fun.plotter.plotter import LinePlotter, TextPlotter, Plotter
from matplotlib import font_manager as fm, axes
import pandas as pd

import numpy as np


class VolatilitySummary(LinePlotter, TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        symbol: str,
        top_ratio: float = 1.0,
        line_color: str = "w",
        line_alpha: float = 0.2,
        line_width: float = 2.5,
        font_color: str = "r",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:

        LinePlotter.__init__(
            self, line_color=line_color, line_alpha=line_alpha, line_width=line_width
        )
        TextPlotter.__init__(
            self,
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._quotes = quotes
        self._frequency = frequency
        self._symbol = symbol

        self._top_ratio = top_ratio

        src = Yahoo()

        if self._symbol in ("es", "spx"):
            self._vix_symbol = "vix"
        elif self._symbol in ("nq", "ndx"):
            self._vix_symbol = "vxn"
        elif self._symbol in ("qr", "sml", "vle"):
            self._vix_symbol = "rvx"
            src = StockCharts()
        elif self._symbol in ("np", "nl", "no", "nikk"):
            self._vix_symbol = "jniv"
            src = InvestingCom()
        elif self._symbol in ("fx", "ezu"):
            self._vix_symbol = "vstx"
            src = InvestingCom()
        elif self._symbol == "hsi":
            self._vix_symbol = "vhsi"
            src = InvestingCom()
        elif self._symbol == "fxi":
            self._vix_symbol = "vxfxi"
            src = InvestingCom()
        elif self._symbol == "cl":
            self._vix_symbol = "ovx"
        elif self._symbol == "gc":
            self._vix_symbol = "gvz"
        # elif self._symbol == "zn":
        #     self._vix_symbol = "tyvix"
        else:
            self._vix_symbol = None
            return

        self._vix_quotes = src.read(
            start=datetime.strptime("19000101", "%Y%m%d"),
            end=datetime.now(),
            symbol=self._vix_symbol,
            frequency=self._frequency,
        ).loc[self._quotes.index[0] : self._quotes.index[-1]]

        assert self._vix_quotes is not None

        # self._line_color = line_color
        # self._line_alpha = line_alpha
        # self._line_width = line_width
        #
        # self._font_color = font_color
        #
        # if font_properties is None:
        #     if font_src is None:
        #         self._font_properties = fm.FontProperties(size=font_size)
        #     else:
        #         self._font_properties = fm.FontProperties(
        #                 fname=font_src, size=font_size
        #         )
        # else:
        #     self._font_properties = font_properties

    def plot(self, ax: axes.Axes) -> None:
        if self._vix_symbol is None:
            return

        mn, mx = ax.get_ylim()

        top = ((mx - mn) * self._top_ratio) + mn

        vix_max = self._vix_quotes.loc[:, "close"].max()
        vix_min = self._vix_quotes.loc[:, "close"].min()

        self._vix_quotes -= vix_min
        self._vix_quotes /= vix_max - vix_min

        self._vix_quotes *= top - mn
        self._vix_quotes += mn

        ax.plot(
            # np.arange(len(self._vix_quotes.index)),
            [
                i
                for i, d in enumerate(self._quotes.index)
                if d in self._vix_quotes.index
            ],
            self._vix_quotes.loc[:, "close"],
            color=self._line_color,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )
