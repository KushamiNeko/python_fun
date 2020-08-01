from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from fun.data.source import FREQUENCY, DAILY
from fun.plotter.plotter import Plotter
from matplotlib import axes


class EntryZone(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        operation: str,
        first_signal: Optional[datetime] = None,
        prepare_signal: Optional[datetime] = None,
        first_to_main_minimum_days: int = 30,
        prepare_minimum_days: int = 5,
        prepare_warning_days: int = 9,
        color_warning: str = "y",
        color_stop: str = "r",
        alpha: float = 0.2,
    ) -> None:
        assert quotes is not None

        assert operation in ("long" "short")

        self._quotes = quotes
        self._frequency = frequency

        self._operation = operation

        self._first_signal = first_signal
        self._prepare_signal = prepare_signal

        self._first_to_main_minimum_days = first_to_main_minimum_days
        self._prepare_minimum_days = prepare_minimum_days
        self._prepare_warning_days = prepare_warning_days

        self._color_warning = color_warning
        self._color_stop = color_stop
        self._alpha = alpha

    def plot(self, ax: axes.Axes) -> None:
        if self._frequency != DAILY:
            return

        mn, mx = ax.get_ylim()

        try:
            if self._first_signal is not None:
                first_signal_index = self._quotes.index.get_loc(self._first_signal)
                minimum_days_index = self._quotes.index.get_loc(
                    self._first_signal
                    + timedelta(days=self._first_to_main_minimum_days),
                    method="nearest",
                )

                ax.bar(
                    first_signal_index,
                    width=minimum_days_index - first_signal_index,
                    bottom=mn,
                    height=mx - mn,
                    align="edge",
                    color=self._color_stop,
                    alpha=self._alpha,
                )

            if self._prepare_signal is not None:
                prepare_signal_index = self._quotes.index.get_loc(self._prepare_signal)
                minimum_days_index = self._quotes.index.get_loc(
                    self._prepare_signal + timedelta(days=self._prepare_minimum_days),
                    method="nearest",
                )
                warning_days_index = self._quotes.index.get_loc(
                    self._prepare_signal + timedelta(days=self._prepare_warning_days),
                    method="nearest",
                )

                ax.bar(
                    prepare_signal_index,
                    width=minimum_days_index - prepare_signal_index,
                    bottom=mn,
                    height=mx - mn,
                    align="edge",
                    color=self._color_stop,
                    alpha=self._alpha,
                )

                ax.bar(
                    minimum_days_index,
                    width=warning_days_index - minimum_days_index,
                    bottom=mn,
                    height=mx - mn,
                    align="edge",
                    color=self._color_warning,
                    alpha=self._alpha,
                )

        except KeyError:
            return
