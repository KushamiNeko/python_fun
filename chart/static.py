import io
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import axes, figure

from fun.chart.base import CHART_SIZE, LARGE_CHART, MEDIUM_CHART, SMALL_CHART, BaseChart
from fun.chart.theme import Theme
from fun.chart.ticker import StepTicker, Ticker, TimeTicker
from fun.trading.transaction import FuturesTransaction


class CandleSticks(BaseChart):
    def __init__(
        self,
        quotes: pd.DataFrame,
        chart_size: CHART_SIZE = LARGE_CHART,
        figsize: Tuple[float, float] = (16.0, 9.0),
    ) -> None:

        assert quotes is not None
        assert chart_size in (LARGE_CHART, MEDIUM_CHART, SMALL_CHART)

        super().__init__(quotes, chart_size)

        if self._chart_size == SMALL_CHART:
            self._figsize = (figsize[0] * 1.0, figsize[1] * 1.0)
        elif self._chart_size == MEDIUM_CHART:
            self._figsize = (figsize[0] * 1.2, figsize[1] * 1.2)
        elif self._chart_size == LARGE_CHART:
            self._figsize = (figsize[0] * 2.0, figsize[1] * 2.0)

        assert self._figsize is not None

        self._theme = Theme()

        self._figure: Optional[figure.Figure] = None
        self._ax: Optional[axes.Axes] = None

    # candlesticks settings
    def _shadow_width(self) -> float:
        if self._chart_size == SMALL_CHART:
            return 1
        elif self._chart_size == MEDIUM_CHART:
            return 1.3
        elif self._chart_size == LARGE_CHART:
            return 2
        else:
            raise ValueError("invalid chart size")

    def _body_width(self) -> float:
        if self._chart_size == SMALL_CHART:
            return 3
        elif self._chart_size == MEDIUM_CHART:
            return 3.9
        elif self._chart_size == LARGE_CHART:
            return 6.5
        else:
            raise ValueError("invalid chart size")

    # general chart settings
    def _linewidth(self) -> float:
        if self._chart_size == SMALL_CHART:
            return 1.0
        elif self._chart_size == MEDIUM_CHART:
            return 1.2
        elif self._chart_size == LARGE_CHART:
            return 2.0
        else:
            raise ValueError("invalid chart size")

    def _tick_fontsize(self) -> float:
        if self._chart_size == SMALL_CHART:
            return 6.0
        elif self._chart_size == MEDIUM_CHART:
            return 7.2
        elif self._chart_size == LARGE_CHART:
            return 15.0
        else:
            raise ValueError("invalid chart size")

    def _text_fontsize(self) -> float:
        if self._chart_size == SMALL_CHART:
            return 5.0
        elif self._chart_size == MEDIUM_CHART:
            return 6.0
        elif self._chart_size == LARGE_CHART:
            return 10.0
        else:
            raise ValueError("invalid chart size")

    def _setup_xticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        loc, labels = ticker.ticks()
        ax.set_xticks(loc)
        ax.set_xticklabels(
            labels, fontproperties=self._theme.get_font(self._tick_fontsize())
        )

    def _setup_yticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        loc, labels = ticker.ticks()
        ax.set_yticks(loc)
        ax.set_yticklabels(
            labels, fontproperties=self._theme.get_font(self._tick_fontsize())
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
            labelsize=self._tick_fontsize(),
        )

        ax.yaxis.tick_right()

    def _plot_text_info(self, ax: axes.Axes, text: str, posx: int = 3) -> None:
        ymin, ymax = self._ylim_from_price_range()
        mid = (ymin + ymax) / 2.0

        y: float
        va: str
        if (
            np.amax(self._quotes.iloc[: int(len(self._quotes) / 6.0)].loc[:, "high"])
            > mid
        ):
            y = np.amin(self._quotes.loc[:, "low"])
            va = "bottom"
        else:
            y = np.amax(self._quotes.loc[:, "high"])
            va = "top"

        ax.text(
            posx,
            y,
            text,
            color=self._theme.get_color("text"),
            fontproperties=self._theme.get_font(self._text_fontsize() * 1.75),
            ha="left",
            va=va,
        )

    def _plot_candlesticks(self, ax: axes.Axes) -> None:

        length = len(self._quotes)
        ax.set_xlim(-0.5, (length - 1) + 0.5)
        ax.set_ylim(*self._ylim_from_price_range())

        for index, df in enumerate(self._quotes.itertuples()):

            p_open = df.open
            p_high = df.high
            p_low = df.low
            p_close = df.close

            p_body_top: float
            p_body_bottom: float

            if p_open > p_close:
                p_body_top = p_open
                p_body_bottom = p_close
            else:
                p_body_top = p_close
                p_body_bottom = p_open

            assert p_body_top is not None
            assert p_body_bottom is not None

            if abs(p_open - p_close) < self._minimum_body_height():
                mid = (p_open + p_close) / 2.0
                mid_height = self._minimum_body_height() / 2.0
                p_body_top = mid + mid_height
                p_body_bottom = mid - mid_height

            color = self._theme.get_color("unchanged")

            if p_close > p_open:
                color = self._theme.get_color("up")
            elif p_close < p_open:
                color = self._theme.get_color("down")

            ax.plot(
                [index, index],
                [p_high, p_low],
                linewidth=self._shadow_width(),
                color=color,
                zorder=5,
            )
            ax.plot(
                [index, index],
                [p_body_top, p_body_bottom],
                linewidth=self._body_width(),
                color=color,
                zorder=5,
            )

        ax.autoscale_view()

    def plot(
        self,
        output: Union[str, io.BytesIO],
        records: Optional[List[FuturesTransaction]] = None,
        show_quote: bool = True,
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
        self._setup_yticks(ax, StepTicker(*self._ylim_from_price_range()))

        self._figure = fig
        self._ax = ax

        self._plot_candlesticks(ax)

        length = len(self._quotes)

        xs = np.arange(length)

        self._plot_indicators(
            lambda ys, cl, al: ax.plot(
                xs,
                ys,
                color=self._theme.get_color(cl),
                alpha=self._theme.get_alpha(al),
                linewidth=self._linewidth(),
            )
        )

        if show_quote:
            quote = self._quotes.iloc[-1]
            self._plot_text_info(
                ax,
                f"Date:  {self._quotes.index[-1].strftime('%Y-%m-%d')}\n"
                f"Open:  {quote.loc['open']:,.2f}\n"
                f"High: {quote.loc['high']:,.2f}\n"
                f"Low: {quote.loc['low']:,.2f}\n"
                f"Close:  {quote.loc['close']:,.2f}\n"
                f"Volume:  {int(quote.get('volume', 0)):,}\n"
                f"Interest:  {int(quote.get('open interest', 0)):,}\n",
            )

        plt.tight_layout()

        if interactive:
            plt.show()
        else:
            plt.savefig(output, dpi=100, facecolor=self._theme.get_color("background"))

        plt.close(fig)

    def to_data_coordinates(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        if self._figure is None or self._ax is None:
            return None

        dx, dy = self._figure.transFigure.transform_point((x, y))
        nx, ny = self._ax.transData.inverted().transform_point((dx, dy))

        min_y, max_y = self._ax.get_ylim()

        nx = int(min(max(round(nx), 0), len(self._quotes) - 1))
        ny = min(max(ny, min_y), max_y)

        return (nx, ny)
