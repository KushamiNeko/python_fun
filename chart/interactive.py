import io
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from bokeh.core.properties import value
from bokeh.layouts import column
from bokeh.models.tools import CrosshairTool, HoverTool, SaveTool
from bokeh.plotting import ColumnDataSource, figure, output_file, save, show

from fun.chart.base import Chart
from fun.chart.theme import InteractiveTheme
from fun.chart.ticker import StepTicker, Ticker, TimeTicker
from fun.trading.transaction import FuturesTransaction


class InteractiveChart(Chart):
    def __init__(
        self,
        quotes: pd.DataFrame,
        figsize: Tuple[float, float] = (1920.0, 1080.0),
        chart_size: str = "l",
    ):
        super().__init__(quotes, chart_size)

        assert self._chart_size in ("m", "l")

        if self._chart_size == "m":
            self._figsize = (figsize[0] * 1.0, figsize[1] * 1.0)
        elif self._chart_size == "l":
            self._figsize = (figsize[0] * 2.0, figsize[1] * 2.0)

        self._theme = InteractiveTheme()

    @property
    def _size_multiplier(self) -> float:
        if self._chart_size == "m":
            return 1.0
        elif self._chart_size == "l":
            return 2.0
        else:
            raise ValueError(f"invalid chart size: {self._chart_size}")

    # candlesticks settings
    @property
    def _shadow_width(self) -> float:
        if self._chart_size == "m":
            return 0.25
        elif self._chart_size == "l":
            return 0.275
        else:
            raise ValueError(f"invalid chart size: {self._chart_size}")

    @property
    def _body_width(self) -> float:
        if self._chart_size == "m":
            return 0.65
        elif self._chart_size == "l":
            return 0.7
        else:
            raise ValueError(f"invalid chart size: {self._chart_size}")

    # general chart settings
    @property
    def _linewidth(self) -> float:
        return 1.5 * self._size_multiplier

    @property
    def _crosshair_linewidth(self) -> float:
        return 2.0 * self._size_multiplier

    @property
    def _tick_fontsize(self) -> str:
        return f"{8.0 * self._size_multiplier}pt"

    @property
    def _text_fontsize(self) -> str:
        return f"{8.0 * self._size_multiplier}pt"

    def _setup_xticks(self, p: figure, ticker: Ticker) -> None:
        xticks = ticker.ticks()

        p.xaxis.ticker = list(xticks.keys())
        p.xaxis.major_label_overrides = xticks

        p.xgrid.ticker = list(xticks.keys())

    def _setup_yticks(self, p: figure, ticker: Ticker) -> None:
        yticks = ticker.ticks()

        p.yaxis.ticker = list(yticks.keys())
        p.yaxis.major_label_overrides = yticks

        p.ygrid.ticker = list(yticks.keys())

    def _setup_general(self, p: figure) -> None:
        p.outline_line_color = None

        p.axis.major_label_text_color = self._theme.get_color("ticks")
        p.axis.major_label_text_font_size = self._tick_fontsize

        p.grid.grid_line_color = self._theme.get_color("grid")
        p.grid.grid_line_alpha = self._theme.get_alpha("grid")

    def _plot_candlesticks(
        self, p: figure, records: Optional[List[FuturesTransaction]] = None
    ) -> None:
        source = ColumnDataSource(
            data=dict(
                x=np.arange(len(self._quotes.index)),
                t=[x.strftime("%Y-%m-%d") for x in self._quotes.index],
                o=self._quotes["open"].to_numpy(),
                h=self._quotes["high"].to_numpy(),
                l=self._quotes["low"].to_numpy(),
                c=self._quotes["close"].to_numpy(),
                sma5=self._quotes["sma5"].to_numpy(),
                sma20=self._quotes["sma20"].to_numpy(),
            )
        )

        tools = [
            CrosshairTool(
                line_width=self._crosshair_linewidth,
                line_color=self._theme.get_color("crosshair"),
                line_alpha=self._theme.get_alpha("crosshair"),
            ),
            HoverTool(
                tooltips=[
                    ("time", "@t"),
                    ("high", "@h{%0.2f}"),
                    ("low", "@l{%0.2f}"),
                    ("open", "@o{%0.2f}"),
                    ("close", "@c{%0.2f}"),
                    ("sma 5", "@sma5{%0.2f}"),
                    ("sma 20", "@sma20{%0.2f}"),
                ],
                formatters={
                    "o": "printf",
                    "h": "printf",
                    "l": "printf",
                    "c": "printf",
                    "sma5": "printf",
                    "sma20": "printf",
                },
                names=["hover"],
            ),
            SaveTool(),
        ]

        p.add_tools(*tools)

        self._setup_general(p)
        self._setup_xticks(p, TimeTicker(self._quotes.index))
        self._setup_yticks(p, StepTicker(*self._ylim_from_price_range()))

        p.vbar(
            x="x",
            width=self._body_width,
            top=self._ylim_from_price_range()[1],
            bottom=self._ylim_from_price_range()[0],
            fill_color="#ff0000",
            line_color="#000000",
            fill_alpha=0,
            line_alpha=0,
            source=source,
            name="hover",
        )

        inc = self._quotes["close"] > self._quotes["open"]
        dec = self._quotes["open"] > self._quotes["close"]
        unc = self._quotes["open"] == self._quotes["close"]

        top, bottom = self._calculate_candlesticks_body_top_bottom()

        p.vbar(
            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[inc].values],
            width=self._body_width,
            top=top[inc],
            bottom=bottom[inc],
            fill_color=self._theme.get_color("up"),
            line_color=self._theme.get_color("up"),
        )

        p.vbar(
            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[inc].values],
            width=self._shadow_width,
            top=self._quotes["high"][inc],
            bottom=self._quotes["low"][inc],
            fill_color=self._theme.get_color("up"),
            line_color=self._theme.get_color("up"),
        )

        p.vbar(
            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[dec].values],
            width=self._body_width,
            top=top[dec],
            bottom=bottom[dec],
            fill_color=self._theme.get_color("down"),
            line_color=self._theme.get_color("down"),
        )

        p.vbar(
            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[dec].values],
            width=self._shadow_width,
            top=self._quotes["high"][dec],
            bottom=self._quotes["low"][dec],
            fill_color=self._theme.get_color("down"),
            line_color=self._theme.get_color("down"),
        )

        p.vbar(
            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[unc].values],
            width=self._body_width,
            top=top[unc],
            bottom=bottom[unc],
            fill_color=self._theme.get_color("unchanged"),
            line_color=self._theme.get_color("unchanged"),
        )

        p.vbar(
            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[unc].values],
            width=self._shadow_width,
            top=self._quotes["high"][unc],
            bottom=self._quotes["low"][unc],
            fill_color=self._theme.get_color("unchanged"),
            line_color=self._theme.get_color("unchanged"),
        )

        if records is not None:
            self._plot_trading_records(
                records,
                lambda x, y, t, ha, va: p.text(
                    x,
                    y,
                    text=value(t),
                    text_align=ha,
                    text_baseline=va,
                    text_color=self._theme.get_color("text"),
                    text_font_size=self._text_fontsize,
                ),
            )

    def futures_price(
        self,
        output: Union[str, io.BytesIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:
        p = figure(
            tools=[],
            plot_width=int(self._figsize[0]),
            plot_height=int(self._figsize[1]),
            y_axis_type="log",
            x_range=(
                0 - self._body_width,
                (len(self._quotes.index) - 1) + self._body_width,
            ),
            y_range=self._ylim_from_price_range(),
            background_fill_color="#000000",
            border_fill_color="#000000",
        )

        self._plot_candlesticks(p, records=records)
        self._plot_indicators(
            lambda col, cl, al: p.line(
                np.arange(len(self._quotes.index)),
                self._quotes[col],
                line_width=self._linewidth,
                line_color=self._theme.get_color(cl),
                line_alpha=self._theme.get_alpha(al),
            )
        )

        if interactive:
            show(p)
        else:
            output_file(output)
            save(p)

    def stocks_price(
        self,
        output: Union[str, io.BytesIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:
        indicator_range = (np.amin(self._quotes["rs"]), np.amax(self._quotes["rs"]))

        p_indicator = figure(
            tools=[],
            plot_width=int(self._figsize[0]),
            plot_height=int(self._figsize[1] * 2.0 / 12.0),
            x_range=(
                0 - self._body_width,
                (len(self._quotes.index) - 1) + self._body_width,
            ),
            y_range=indicator_range,
            background_fill_color="#000000",
            border_fill_color="#000000",
        )

        self._setup_general(p_indicator)
        self._setup_xticks(p_indicator, TimeTicker(self._quotes.index))
        self._setup_yticks(
            p_indicator,
            StepTicker(indicator_range[0], indicator_range[1], nbins=5, steps=None),
        )

        p_indicator.line(
            np.arange(len(self._quotes.index)),
            self._quotes["rs"],
            line_width=self._linewidth,
            line_color=self._theme.get_color("in0"),
        )

        p_price = figure(
            tools=[],
            plot_width=int(self._figsize[0]),
            plot_height=int(self._figsize[1] * 10.0 / 12.0),
            y_axis_type="log",
            x_range=(
                0 - self._body_width,
                (len(self._quotes.index) - 1) + self._body_width,
            ),
            y_range=self._ylim_from_price_range(),
            background_fill_color="#000000",
            border_fill_color="#000000",
        )

        self._plot_candlesticks(p_price, records=records)
        self._plot_indicators(
            lambda col, cl, al: p_price.line(
                np.arange(len(self._quotes.index)),
                self._quotes[col],
                line_width=self._linewidth,
                line_color=self._theme.get_color(cl),
                line_alpha=self._theme.get_alpha(al),
            )
        )

        if interactive:
            show(column(p_indicator, p_price))
        else:
            output_file(output)
            save(column(p_indicator, p_price))
