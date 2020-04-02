import io
from typing import List, Optional, Tuple, Union

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import axes, figure

from fun.chart import base
from fun.chart.base import CHART_SIZE, LARGE_CHART, MEDIUM_CHART, SMALL_CHART
from fun.chart.setting import CandleSticksSetting
from fun.chart.theme import Theme
from fun.chart.ticker import StepTicker, Ticker, TimeTicker
from fun.plotter.candlesticks import CandleSticks as CandleSticksPlotter
from fun.plotter.plotter import Plotter

matplotlib.use("agg")


class CandleSticks(base.CandleSticks):
    def __init__(
        self,
        quotes: pd.DataFrame,
        chart_size: CHART_SIZE = LARGE_CHART,
        figsize: Tuple[float, float] = (16.0, 9.0),
    ) -> None:

        assert quotes is not None
        assert chart_size in (LARGE_CHART, MEDIUM_CHART)

        super().__init__(quotes)

        if chart_size == SMALL_CHART:
            self._figsize = (figsize[0] * 1.0, figsize[1] * 1.0)
        elif chart_size == MEDIUM_CHART:
            self._figsize = (figsize[0] * 1.2, figsize[1] * 1.2)
        elif chart_size == LARGE_CHART:
            self._figsize = (figsize[0] * 2.0, figsize[1] * 2.0)

        assert self._figsize is not None

        self._theme = Theme()
        self._setting = CandleSticksSetting(chart_size)

        self._figure: Optional[figure.Figure] = None
        self._ax: Optional[axes.Axes] = None

    def _setup_xticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        loc, labels = ticker.ticks()
        ax.set_xticks(loc)
        ax.set_xticklabels(
            labels, fontproperties=self._theme.get_font(self._setting.tick_fontsize())
        )

    def _setup_yticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        loc, labels = ticker.ticks()
        ax.set_yticks(loc)
        ax.set_yticklabels(
            labels, fontproperties=self._theme.get_font(self._setting.tick_fontsize())
        )

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
            labelsize=self._setting.tick_fontsize(),
        )

        ax.yaxis.tick_right()

    # def _plot_candlesticks(self, ax: axes.Axes) -> None:
    # ax.set_xlim(*self.chart_xrange())
    # ax.set_ylim(*self.chart_yrange())

    # for index, df in enumerate(self._quotes.itertuples()):

    # p_open = df.open
    # p_high = df.high
    # p_low = df.low
    # p_close = df.close

    # p_body_top: float
    # p_body_bottom: float

    # if p_open > p_close:
    # p_body_top = p_open
    # p_body_bottom = p_close
    # else:
    # p_body_top = p_close
    # p_body_bottom = p_open

    # assert p_body_top is not None
    # assert p_body_bottom is not None

    # if abs(p_open - p_close) < self._minimum_height():
    # mid = (p_open + p_close) / 2.0
    # mid_height = self._minimum_height() / 2.0
    # p_body_top = mid + mid_height
    # p_body_bottom = mid - mid_height

    # color = self._theme.get_color("unchanged")

    # if p_close > p_open:
    # color = self._theme.get_color("up")
    # elif p_close < p_open:
    # color = self._theme.get_color("down")

    # ax.plot(
    # [index, index],
    # [p_high, p_low],
    # linewidth=self._setting.shadow_width(),
    # color=color,
    # zorder=5,
    # )
    # ax.plot(
    # [index, index],
    # [p_body_top, p_body_bottom],
    # linewidth=self._setting.body_width(),
    # color=color,
    # zorder=5,
    # )

    # ax.autoscale_view()

    def to_data_coordinates(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        if self._figure is None or self._ax is None:
            return None

        dx, dy = self._figure.transFigure.transform_point((x, y))
        nx, ny = self._ax.transData.inverted().transform_point((dx, dy))

        min_y, max_y = self._ax.get_ylim()

        nx = int(min(max(round(nx), 0), len(self._quotes) - 1))
        ny = min(max(ny, min_y), max_y)

        return (nx, ny)

    def render(
        self,
        output: Optional[Union[str, io.BytesIO]] = None,
        plotters: Optional[List[Plotter]] = None,
        interactive: bool = False,
    ) -> None:

        fig, ax = plt.subplots(
            figsize=self._figsize,
            facecolor=self._theme.get_color("background"),
            tight_layout=False,
        )

        ax.set_yscale("log")

        self._setup_general(fig, ax)
        self._setup_xticks(ax, TimeTicker(self._quotes))
        self._setup_yticks(ax, StepTicker(*self.chart_yrange()))

        self._figure = fig
        self._ax = ax

        ax.set_xlim(*self.chart_xrange())
        ax.set_ylim(*self.chart_yrange())

        # self._plot_candlesticks(ax)

        CandleSticksPlotter(
            quotes=self._quotes,
            shadow_width=self._setting.shadow_width(),
            body_width=self._setting.body_width(),
            minimum_height=self._minimum_height(),
            color_up=self._theme.get_color("up"),
            color_down=self._theme.get_color("down"),
            color_unchanged=self._theme.get_color("unchanged"),
        ).plot(ax)

        ax.autoscale_view()

        if plotters is not None and len(plotters) > 0:
            for p in plotters:
                p.plot(ax)

        plt.tight_layout()

        if interactive:
            plt.show()
        else:
            assert output is not None
            plt.savefig(output, dpi=100, facecolor=self._theme.get_color("background"))

        plt.close(fig)
