from datetime import timedelta, datetime
from typing import List, Optional, NewType

import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.data.source import FREQUENCY, WEEKLY, Yahoo, DAILY
from fun.plotter.plotter import TextPlotter
from fun.trading.transaction import FuturesTransaction
from fun.utils import pretty, colors

DAY_ACTION = NewType("DAY_ACTION", int)
FOLLOW_THROUGH = DAY_ACTION(0)
DISTRIBUTION = DAY_ACTION(1)
NEUTRAL = DAY_ACTION(2)


class DistributionsDay(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        reference_symbols: List[str] = ["spx", "compq", "sml"],
        distribution_threshold: float = -0.2,
        # follow_through_threshold: float=1.0,
        distribution_invalid_threshold: float = 5.0,
        distribution_color: str = "r",
        days_pass_invalid_threshold: int = 35,
        invalid_distribution_color: str = "r",
        # follow_through_color: str="g",
        xoffset: float = 3,
        font_color: str = "r",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
        info_font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._quotes = quotes
        self._frequency = frequency

        self._reference_symbols = reference_symbols

        self._distribution_threshold = distribution_threshold
        # self._follow_through_threshold = follow_through_threshold

        self._distribution_color = distribution_color
        self._invalid_distribution_color = invalid_distribution_color
        # self._follow_through_color = follow_through_color

        if info_font_properties is None:
            self._info_font_properties = font_properties
        else:
            self._info_font_properties = info_font_properties

        self._xoffset = xoffset

        self._days_pass_invalid_threshold = days_pass_invalid_threshold
        self._distribution_invalid_threshold = distribution_invalid_threshold

        self._dataframes = {}

        src = Yahoo()

        for symbol in self._reference_symbols:
            self._dataframes[symbol] = src.read(
                start=datetime.strptime("19000101", "%Y%m%d"),
                end=datetime.utcnow() + timedelta(days=2),
                symbol=symbol,
                frequency=self._frequency,
            ).loc[self._quotes.index[0] : self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:
        if self._frequency != DAILY:
            return

        assert ax is not None

        counts = {}

        for x in range(len(self._quotes.index)):
            if x == 0:
                continue

            labels = []
            action = NEUTRAL
            color = self._invalid_distribution_color
            for key, quotes in self._dataframes.items():
                index = self._quotes.index[x]
                if index not in quotes.index:
                    pretty.color_print(
                        colors.PAPER_AMBER_300, f"skip {index} in {key}",
                    )
                    continue

                current_close = quotes.loc[index, "close"]
                current_volume = quotes.loc[index, "volume"]

                index = self._quotes.index[x - 1]
                if index not in quotes.index:
                    pretty.color_print(
                        colors.PAPER_AMBER_300, f"skip {index} in {key}",
                    )
                    continue

                previous_close = quotes.loc[index, "close"]
                previous_volume = quotes.loc[index, "volume"]

                if current_close <= 0 or previous_close <= 0:
                    continue

                if current_volume <= 0 or previous_volume <= 0:
                    continue

                move = ((current_close - previous_close) / previous_close) * 100.0
                # qualified = False

                if (
                    move < self._distribution_threshold
                    and current_volume > previous_volume
                ):
                    action = DISTRIBUTION
                    # elif move > self._follow_through_threshold and current_volume > previous_volume:
                    #     action = FOLLOW_THROUGH

                    for k in key:
                        if k.upper() not in labels:
                            labels.append(k.upper())
                            break

                    # labels.append(key[0].upper())

                    if (
                        self._quotes.index[-1] - self._quotes.index[x]
                    ).days < self._days_pass_invalid_threshold:
                        # lc = self._quotes.iloc[-1].get("close")
                        # if (((lc - current_close) / current_close) * 100.0) < self._distribution_invalid_threshold:

                        color = self._distribution_color
                        if key in counts:
                            counts[key] += 1
                        else:
                            counts[key] = 1

            if action != NEUTRAL:
                highs = self._quotes.loc[:, "high"]
                lows = self._quotes.loc[:, "low"]

                mx = highs.max()
                mn = lows.min()
                mr = mx - mn

                middle = (mx + mn) / 2.0

                h = highs.iloc[x]
                l = lows.iloc[x]
                m = (h + l) / 2.0

                offset = mr * 0.0075

                # y = l * (1 - offset) if m > middle else h * (1 + offset)

                y = l - offset if m < middle else h + offset
                va = "top" if m < middle else "bottom"

                arrow = "↑" if action == FOLLOW_THROUGH else "↓"

                labels.append(arrow)

                text = "\n".join(labels)

                # color = (
                #     self._distribution_color
                #     if action == DISTRIBUTION
                #     else self._follow_through_color
                # )

                ax.text(
                    x,
                    y,
                    text,
                    color=color,
                    # color=self._font_color,
                    fontproperties=self._font_properties,
                    ha="center",
                    va=va,
                )

        if len(self._quotes) > 1:
            text = "\n".join(
                f"{k.upper()}: {counts[k]}" for k in self._reference_symbols
            )

            h = np.amax(self._quotes.loc[:, "high"])
            l = np.amin(self._quotes.loc[:, "low"])

            lh = np.amax(self._quotes.iloc[-30:].loc[:, "high"])
            ll = np.amin(self._quotes.iloc[-30:].loc[:, "low"])

            y: float
            va: str
            if abs(l - ll) > abs(h - lh):
                y = np.amin(self._quotes.loc[:, "low"])
                va = "bottom"
            else:
                y = np.amax(self._quotes.loc[:, "high"])
                va = "top"

            ax.text(
                len(self._quotes.index) - self._xoffset,
                y,
                text,
                color=self._font_color,
                fontproperties=self._info_font_properties,
                ha="right",
                va=va,
            )
