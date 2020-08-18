from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.data.source import FREQUENCY
from fun.plotter.plotter import Plotter
from fun.plotter.volatility import VolatilitySource
from fun.utils import colors


class Level(VolatilitySource, Plotter):
    def __init__(
        self,
        full_quotes: pd.DataFrame,
        quotes: pd.DataFrame,
        symbol: str,
        frequency: FREQUENCY,
        x_offset: float = 3,
        # yellow_threshold: float = 22.5,
        # red_threshold: float = 45.0,
        color_green: str = colors.PAPER_LIGHT_GREEN_A200,
        color_yellow: str = colors.PAPER_AMBER_A200,
        color_red: str = colors.PAPER_PINK_A100,
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert full_quotes is not None
        assert quotes is not None

        if font_properties is None:
            if font_src is None:
                self._font_properties = fm.FontProperties(size=font_size)
            else:
                self._font_properties = fm.FontProperties(
                    fname=font_src, size=font_size
                )
        else:
            self._font_properties = font_properties

        VolatilitySource.__init__(self, symbol=symbol)

        self._full_quotes = full_quotes

        self._quotes = quotes
        self._frequency = frequency

        self._x_offset = x_offset

        # self._yellow_threshold = yellow_threshold
        # self._red_threshold = red_threshold

        self._color_green = color_green
        self._color_yellow = color_yellow
        self._color_red = color_red

        self._vix_quotes = None
        if self._vix_symbol is not None and self._src is not None:
            self._vix_quotes = self._src.read(
                start=datetime.strptime("19000101", "%Y%m%d"),
                end=datetime.now(),
                symbol=self._vix_symbol,
                frequency=self._frequency,
            ).loc[self._quotes.index[0] : self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:

        h = np.amax(self._quotes.loc[:, "high"])
        l = np.amin(self._quotes.loc[:, "low"])

        lh = np.amax(self._quotes.iloc[-30:].loc[:, "high"])
        ll = np.amin(self._quotes.iloc[-30:].loc[:, "low"])

        mn, mx = ax.get_ylim()

        x = len(self._quotes.index) - self._x_offset

        y = mx
        va = "top"
        if abs(l - ll) > abs(h - lh):
            y = mn
            va = "bottom"

        ha = "right"

        self._plot_volatility_level(ax=ax, x=x, y=y, ha=ha, va=va, ending="\n")
        self._plot_moving_average_distance(ax=ax, x=x, y=y, ha=ha, va=va)

    def _plot_moving_average_distance(
        self,
        ax: axes.Axes,
        x: float,
        y: float,
        ha: str,
        va: str,
        n: int = 300,
        yellow_threshold: float = 9.0,
        red_threshold: float = 12.0,
        ending: str = "",
    ) -> None:

        ma = self._full_quotes.loc[:, "close"].rolling(n).mean().iloc[-1]
        c = self._quotes.iloc[-1].get("close")

        if c < ma:
            return

        p = ((c - ma) / ma) * 100.0

        color = self._color_green
        if p > yellow_threshold:
            color = self._color_yellow
        if p > red_threshold:
            color = self._color_red

        ax.text(
            x,
            y,
            f"Δ {n} MA: {p:.2f}%{ending}",
            color=color,
            fontproperties=self._font_properties,
            ha=ha,
            va=va,
        )

    def _plot_volatility_level(
        self,
        ax: axes.Axes,
        x: float,
        y: float,
        ha: str,
        va: str,
        yellow_threshold: float = 22.5,
        red_threshold: float = 45.0,
        ending: str = "",
    ) -> None:
        if self._vix_symbol is None or self._vix_quotes is None:
            return

        if len(self._vix_quotes.index) == 0:
            return

        value = self._vix_quotes.iloc[-1].get("close", None)
        if value is None:
            return

        color = self._color_green
        # if value > self._yellow_threshold:
        if value > yellow_threshold:
            color = self._color_yellow

        # if value > self._red_threshold:
        if value > red_threshold:
            color = self._color_red

        ax.text(
            x,
            y,
            f"{self._vix_symbol.upper()}: {value:.2f}{ending}",
            color=color,
            fontproperties=self._font_properties,
            ha=ha,
            va=va,
        )
