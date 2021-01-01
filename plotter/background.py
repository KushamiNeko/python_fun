import pandas as pd
from fun.data.source import DAILY, FREQUENCY, MONTHLY, WEEKLY
from fun.plotter.plotter import Plotter
from matplotlib import axes


class BackgroundTimeRangeMark(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        from_start: bool = True,
        color: str = "w",
        alpha: float = 0.075,
    ) -> None:
        self._quotes = quotes
        self._frequency = frequency
        self._from_start = from_start
        self._color = color
        self._alpha = alpha

    def plot(self, ax: axes.Axes) -> None:
        if self._frequency == DAILY or self._frequency == WEEKLY:
            self._monthly_range(ax)
        elif self._frequency == MONTHLY:
            self._yearly_range(ax)

    def _time_range(self, ax: axes.Axes, range_type: str) -> None:
        anchor_x = 0

        assert range_type in ("m", "y")
        if range_type == "m":
            current = self._quotes.index[0].to_pydatetime().month
        elif range_type == "y":
            current = self._quotes.index[0].to_pydatetime().year

        plotting = self._from_start

        mn, mx = ax.get_ylim()

        for i, x in enumerate(self._quotes.index):

            if range_type == "m":
                cursor = x.to_pydatetime().month
            elif range_type == "y":
                cursor = x.to_pydatetime().year

            if cursor != current:
                plotting = not plotting
                current = cursor

                if plotting is False:
                    ax.bar(
                        anchor_x,
                        width=i - anchor_x,
                        bottom=mn,
                        height=mx - mn,
                        align="edge",
                        color=self._color,
                        alpha=self._alpha,
                    )
                else:
                    anchor_x = i

        if plotting is True:
            ax.bar(
                anchor_x,
                width=(len(self._quotes) - 1) - anchor_x,
                bottom=mn,
                height=mx - mn,
                align="edge",
                color=self._color,
                alpha=self._alpha,
            )

    def _monthly_range(self, ax: axes.Axes) -> None:
        self._time_range(ax, "m")

    def _yearly_range(self, ax: axes.Axes) -> None:
        self._time_range(ax, "y")
