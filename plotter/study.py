import json
import os
from datetime import datetime

import pandas as pd
from matplotlib import axes

from fun.data.source import FREQUENCY
from fun.plotter.plotter import Plotter
from fun.utils import colors, pretty


class StudyZone(Plotter):
    def __init__(
        self,
        symbol: str,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        color_long_entry: str = colors.PAPER_PURPLE_400,
        color_short_entry: str = colors.PAPER_INDIGO_400,
        color_close: str = colors.PAPER_GREEN_400,
        alpha: float = 0.25,
    ) -> None:
        assert quotes is not None

        root = os.path.join(os.getenv("HOME"), "Documents", "TRADING_NOTES", "studies")
        path = os.path.join(root, f"{symbol.lower()}.json")

        self._symbol = symbol
        self._quotes = quotes
        self._frequency = frequency

        self._studies = None
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    self._studies = json.load(f)
                except json.JSONDecodeError:
                    pretty.color_print(
                        colors.PAPER_RED_400,
                        f"invalid json file for trading study: {path}",
                    )
                    self._studies = None

        self._color_long_entry = color_long_entry
        self._color_short_entry = color_short_entry
        self._color_close = color_close
        self._alpha = alpha

    def plot(self, ax: axes.Axes) -> None:
        if self._studies is None:
            return

        mn, mx = ax.get_ylim()

        for study in self._studies:
            start = datetime.strptime(study["start"], "%Y%m%d")
            end = datetime.strptime(study["end"], "%Y%m%d")

            start_index = self._quotes.index.get_loc(
                start,
                method="nearest",
            )

            end_index = self._quotes.index.get_loc(
                end,
                method="nearest",
            )

            color = ""
            if study["operation"] == "long":
                color = self._color_long_entry
            elif study["operation"] == "short":
                color = self._color_short_entry
            elif study["operation"] == "close":
                color = self._color_close
            else:
                raise ValueError(f"invalid study operation: {study['operation']}")

            ax.bar(
                start_index,
                width=end_index - start_index,
                bottom=mn,
                height=mx - mn,
                align="edge",
                color=color,
                alpha=self._alpha,
            )
