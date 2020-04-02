import pandas as pd
from matplotlib import axes

from fun.plotter.plotter import Plotter


class CandleSticks(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        shadow_width: float,
        body_width: float,
        minimum_height: float,
        color_up: str,
        color_down: str,
        color_unchanged: str,
    ):
        self._quotes = quotes
        self._shadow_width = shadow_width
        self._body_width = body_width
        self._minimum_height = minimum_height
        self._color_up = color_up
        self._color_down = color_down
        self._color_unchanged = color_unchanged

    def plot(self, ax: axes.Axes) -> None:
        # ax.set_xlim(*self.chart_xrange())
        # ax.set_ylim(*self.chart_yrange())

        for index, df in enumerate(self._quotes.itertuples()):

            p_open = df.open
            p_high = df.high
            p_low = df.low
            p_close = df.close

            p_shadow_top = p_high
            p_shadow_bottom = p_low

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

            if abs(p_open - p_close) < self._minimum_height:
                mid = (p_open + p_close) / 2.0
                mid_height = self._minimum_height / 2.0
                p_body_top = mid + mid_height
                p_body_bottom = mid - mid_height

            if abs(p_shadow_top - p_shadow_bottom) < self._minimum_height:
                mid = (p_shadow_top + p_shadow_bottom) / 2.0
                mid_height = self._minimum_height / 2.0
                p_shadow_top = mid + mid_height
                p_shadow_bottom = mid - mid_height

            color = self._color_unchanged

            if p_close > p_open:
                color = self._color_up
            elif p_close < p_open:
                color = self._color_down

            ax.plot(
                [index, index],
                [p_shadow_top, p_shadow_bottom],
                linewidth=self._shadow_width,
                color=color,
                zorder=5,
            )
            ax.plot(
                [index, index],
                [p_body_top, p_body_bottom],
                linewidth=self._body_width,
                color=color,
                zorder=5,
            )

        # ax.autoscale_view()
