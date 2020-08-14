from datetime import timedelta
from typing import List, Optional, Tuple
from datetime import datetime
import numpy as np
import pandas as pd
from fun.data.source import FREQUENCY, WEEKLY
from fun.plotter.plotter import TextPlotter
from fun.trading.transaction import FuturesTransaction
from fun.trading.agent import TradingAgent
from matplotlib import axes, font_manager as fm


class LeverageRecords(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        # records: List[FuturesTransaction],
        book_title: str,
        agent: TradingAgent,
        flip_position: bool = False,
        font_color: str = "k",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
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

        # self._records = records
        self._records = agent.read_records(title=book_title)

        self._flip_position = flip_position

    def plot(self, ax: axes.Axes) -> None:
        if len(self._quotes) == 0:
            return

        if self._records is None or len(self._records) == 0:
            return

        assert ax is not None

        dates = self._quotes.index
        ops = np.add.accumulate(
            [float(f"{r.operation()}{r.leverage()}") for r in self._records]
        )

        ops_s = -1
        ops_e = -1

        loc = []
        for i, r in enumerate(self._records):
            tar = r.datetime()
            if self._frequency == WEEKLY:
                tar = tar - timedelta(days=tar.weekday())

            if ops_s == -1 and tar >= dates[0]:
                ops_s = i
            if ops_e == -1 and tar > dates[-1]:
                ops_e = i

            where = np.argwhere(dates == tar).flatten()
            if where.size != 0:
                loc.append(where.min())

        if ops_s == -1:
            return

        if ops_e == -1:
            ops_e = len(self._records)

        ops = ops[ops_s:ops_e]

        if len(ops) == 0:
            return

        loc = np.array(loc)

        unique, count = np.unique(loc, return_counts=True)
        labels = np.where(
            ops == 0,
            "X",
            np.vectorize(lambda v: f"{v[0].strip()}\n{v[1:].strip()}")(
                np.vectorize(lambda v: f"L{abs(v):.0f}" if v > 0 else f"S{abs(v):.0f}")(
                    ops
                )
            ),
        )

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]

        mx = highs.max()
        mn = lows.min()
        mr = mx - mn

        middle = (mx + mn) / 2.0

        offset = mr * 0.0075

        for x in unique:
            h = highs.iloc[x]
            l = lows.iloc[x]
            m = (h + l) / 2.0

            va = "top" if m > middle else "bottom"
            if self._flip_position:
                va = "bottom" if va == "top" else "top"

            # y = l - offset if m > middle else h + offset
            y = l - offset if va == "top" else h + offset

            text = "\n".join([labels[j] for j in np.argwhere(loc == x).flatten()])

            ax.text(
                x,
                y,
                text,
                color=self._font_color,
                fontproperties=self._font_properties,
                ha="center",
                va=va,
            )


class LongShortLeverageRecords(TextPlotter):
    def __init__(
        self,
        dtime: datetime,
        virtual_close: float,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        long_book_title: str,
        short_book_title: str,
        agent: TradingAgent,
        font_color: str = "k",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
        info_font_color: str = "k",
        info_font_size: float = 10.0,
        info_font_src: Optional[str] = None,
        info_font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._font_size = font_size
        self._font_src = font_src

        self._info_font_color = info_font_color
        self._info_font_size = info_font_size
        self._info_font_src = info_font_src

        if info_font_properties is None:
            if info_font_src is None:
                self._info_font_properties = fm.FontProperties(size=font_size)
            else:
                self._info_font_properties = fm.FontProperties(
                    fname=info_font_src, size=info_font_size
                )
        else:
            self._info_font_properties = info_font_properties

        self._dtime = dtime
        self._virtual_close = virtual_close
        self._quotes = quotes
        self._frequency = frequency

        self._long_book_title = long_book_title
        self._short_book_title = short_book_title

        self._agent = agent

    def plot(self, ax: axes.Axes) -> None:
        long_leverage = self._agent.open_positions_leverage(
            title=self._long_book_title, dtime=self._dtime
        )
        long_virtual_pl = self._agent.open_positions_virtual_pl(
            title=self._long_book_title,
            dtime=self._dtime,
            virtual_close=self._virtual_close,
        )

        plotter = LeverageRecords(
            quotes=self._quotes,
            frequency=self._frequency,
            book_title=self._long_book_title,
            agent=self._agent,
            font_color=self._font_color,
            font_size=self._font_size,
            font_src=self._font_src,
            font_properties=self._font_properties,
        )

        plotter.plot(ax)

        short_leverage = self._agent.open_positions_leverage(
            title=self._short_book_title, dtime=self._dtime,
        )
        short_virtual_pl = self._agent.open_positions_virtual_pl(
            title=self._short_book_title,
            dtime=self._dtime,
            virtual_close=self._virtual_close,
        )

        plotter = LeverageRecords(
            quotes=self._quotes,
            frequency=self._frequency,
            book_title=self._short_book_title,
            agent=self._agent,
            flip_position=True,
            font_color=self._font_color,
            font_size=self._font_size,
            font_src=self._font_src,
            font_properties=self._font_properties,
        )

        plotter.plot(ax)

        long_leverage = long_leverage if long_leverage is not None else 0
        short_leverage = short_leverage if short_leverage is not None else 0

        nominal_long_vpl = long_virtual_pl[0] if long_virtual_pl is not None else 0
        leveraged_long_vpl = long_virtual_pl[1] if long_virtual_pl is not None else 0

        nominal_short_vpl = short_virtual_pl[0] if short_virtual_pl is not None else 0
        leveraged_short_vpl = short_virtual_pl[1] if short_virtual_pl is not None else 0

        nominal_balance = nominal_long_vpl + nominal_short_vpl
        leveraged_balance = leveraged_long_vpl + leveraged_short_vpl

        text = "\n".join(
            [
                "Long : Short",
                "============",
                f"{long_leverage} : {short_leverage}",
                "============",
                f"{nominal_long_vpl: .2f}% : {nominal_short_vpl: .2f}%",
                f"{leveraged_long_vpl: .2f}% : {leveraged_short_vpl: .2f}%",
                "============",
                f"{nominal_balance: .2f}%",
                f"{leveraged_balance: .2f}%",
            ]
        )

        ax.text(
            len(self._quotes.index) // 2,
            ax.get_ylim()[0],
            text,
            color=self._info_font_color,
            fontproperties=self._info_font_properties,
            ha="center",
            va="bottom",
        )

