import io
import re
from typing import Any, List, Optional, Tuple, Union, cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import axes, figure, patches
from matplotlib.collections import PatchCollection

from fun.chart.base import Chart
from fun.chart.theme import Theme
from fun.chart.ticker import StepTicker, Ticker, TimeTicker
from fun.trading.transaction import FuturesTransaction


class StaticChart(Chart):
    def __init__(
        self,
        quotes: pd.DataFrame,
        figsize: Tuple[float, float] = (16.0, 9.0),
        chart_size: str = "l",
    ):
        super().__init__(quotes, chart_size)

        assert self._chart_size in ("m", "l")

        if self._chart_size == "m":
            self._figsize = (figsize[0] * 1.2, figsize[1] * 1.2)
        elif self._chart_size == "l":
            self._figsize = (figsize[0] * 2.0, figsize[1] * 2.0)

        self._theme = Theme()

    @property
    def _size_multiplier(self) -> float:
        if self._chart_size == "m":
            return 1.2
        elif self._chart_size == "l":
            return 2.0
        else:
            raise ValueError(f"invalid chart size: {self._chart_size}")

    # candlesticks settings
    @property
    def _shadow_width(self) -> float:
        return 0.2

    @property
    def _body_width(self) -> float:
        return 0.6

    # general chart settings
    @property
    def _linewidth(self) -> float:
        return 0.75 * self._size_multiplier

    @property
    def _tick_fontsize(self) -> str:
        return f"{5.5 * self._size_multiplier}"

    @property
    def _text_fontsize(self) -> str:
        return f"{5 * self._size_multiplier}"

    def _setup_xticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        ticks = ticker.ticks()
        ax.set_xticks(list(ticks.keys()))
        ax.set_xticklabels(list(ticks.values()))

    def _setup_yticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        ticks = ticker.ticks()
        ax.set_yticks(list(ticks.keys()))
        ax.set_yticklabels(list(ticks.values()))

    def _setup_general(self, fig: figure.Figure, ax: axes.Axes) -> None:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.grid(
            True,
            color=self._theme.get_color("grid"),
            alpha=self._theme.get_alpha("grid"),
        )

        ax.set_axisbelow(True)

        fig.set_facecolor(self._theme.get_color("background"))
        ax.set_facecolor(self._theme.get_color("background"))

        ax.tick_params(
            axis="both",
            color=self._theme.get_color("ticks"),
            labelcolor=self._theme.get_color("ticks"),
            labelsize=self._tick_fontsize,
        )

    def _plot_candlesticks(
        self, ax: axes.Axes, records: Optional[List[FuturesTransaction]] = None
    ) -> None:
        ax.set_xlim(-self._body_width, (len(self._quotes.index) - 1) + self._body_width)
        ax.set_ylim(*self._ylim_from_price_range())

        bodys = []
        shadows = []

        body_offset = self._body_width / 2.0
        shadow_offset = self._shadow_width / 2.0

        top, bottom = self._calculate_candlesticks_body_top_bottom()

        for t in np.arange(len(self._quotes.index)):

            p_open = self._quotes.iloc[t]["open"]
            p_high = self._quotes.iloc[t]["high"]
            p_low = self._quotes.iloc[t]["low"]
            p_close = self._quotes.iloc[t]["close"]

            p_top = top[t]
            p_bottom = bottom[t]

            color = self._theme.get_color("unchanged")

            if p_close > p_open:
                color = self._theme.get_color("up")
            elif p_close < p_open:
                color = self._theme.get_color("down")

            shadow = patches.Rectangle(
                xy=(t - shadow_offset, p_low),
                width=self._shadow_width,
                height=p_high - p_low,
                facecolor=color,
                edgecolor=color,
            )

            body = patches.Rectangle(
                xy=(t - body_offset, p_bottom),
                width=self._body_width,
                height=p_top - p_bottom,
                facecolor=color,
                edgecolor=color,
            )

            bodys.append(body)
            shadows.append(shadow)

        ax.add_collection(PatchCollection(bodys, match_original=True, zorder=5))

        ax.add_collection(PatchCollection(shadows, match_original=True, zorder=5))

        if records is not None:
            self._plot_trading_records(
                records,
                lambda x, y, t, ha, va: ax.text(
                    x,
                    y,
                    t,
                    ha=ha,
                    va=va,
                    fontsize=self._text_fontsize,
                    color=self._theme.get_color("text"),
                ),
            )

        ax.autoscale_view()

    def futures_price(
        self,
        output: Union[str, io.BytesIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:
        fig, ax = plt.subplots(
            figsize=self._figsize,
            facecolor=self._theme.get_color("background"),
            tight_layout=False,
        )

        ax.set_yscale("log")

        self._setup_general(fig, ax)
        self._setup_xticks(ax, TimeTicker(self._quotes.index))
        self._setup_yticks(ax, StepTicker(*self._ylim_from_price_range()))

        self._plot_candlesticks(ax, records=records)
        self._plot_indicators(
            lambda col, cl, al: ax.plot(
                self._quotes[col].to_numpy(),
                color=self._theme.get_color(cl),
                alpha=self._theme.get_alpha(al),
                linewidth=self._linewidth,
            )
        )

        plt.tight_layout()

        if interactive:
            plt.show()
        else:
            plt.savefig(output, dpi=100, facecolor=self._theme.get_color("background"))

        plt.close(fig)

    def stocks_price(
        self,
        output: Union[str, io.BytesIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:

        fig = plt.figure(
            figsize=self._figsize, facecolor=self._theme.get_color("background")
        )

        grid = plt.GridSpec(12, 1)

        ax = fig.add_subplot(grid[2:, 0])
        ax.set_yscale("log")

        self._setup_general(fig, ax)
        self._setup_xticks(ax, TimeTicker(self._quotes.index))
        self._setup_yticks(ax, StepTicker(*self._ylim_from_price_range()))

        self._plot_candlesticks(ax, records=records)

        self._plot_indicators(
            lambda col, cl, al: ax.plot(
                self._quotes[col].to_numpy(),
                color=self._theme.get_color(cl),
                alpha=self._theme.get_alpha(al),
                linewidth=self._linewidth,
            )
        )

        in_ax = fig.add_subplot(grid[:2, 0], sharex=ax)
        in_ax.set_yscale("linear")

        self._setup_general(fig, in_ax)
        self._setup_yticks(
            in_ax,
            StepTicker(
                np.amin(self._quotes["rs"]),
                np.amax(self._quotes["rs"]),
                nbins=5,
                steps=None,
            ),
        )

        in_ax.plot(
            self._quotes["rs"].to_numpy(),
            color=self._theme.get_color("in0"),
            linewidth=self._linewidth,
        )

        in_ax.autoscale_view()

        plt.tight_layout()

        if interactive:
            plt.show()
        else:
            plt.savefig(output, dpi=100, facecolor=self._theme.get_color("background"))

        plt.close(fig)
