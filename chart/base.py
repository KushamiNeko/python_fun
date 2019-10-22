import io
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from fun.trading.transaction import FuturesTransaction


class Chart(metaclass=ABCMeta):
    def __init__(self, quotes: pd.DataFrame, chart_size: str = "l"):

        assert quotes is not None
        assert re.match(r"^m|l$", chart_size.lower())

        self._quotes = quotes
        self._chart_size = chart_size.lower()

    @property
    def _body_min_height(self) -> float:
        mn, mx = self._ylim_from_price_range()
        r = mx - mn

        # return r * 0.001
        return r * 0.002

    @property
    def _price_range_extend_ratio(self) -> float:
        return 25.0

    def _ylim_from_price_range(self) -> Tuple[float, float]:
        mn = np.amin(self._quotes["low"].to_numpy())
        mx = np.amax(self._quotes["high"].to_numpy())

        r = mx - mn

        return (
            mn - (r / self._price_range_extend_ratio),
            mx + (r / self._price_range_extend_ratio),
        )

    def _calculate_candlesticks_body_top_bottom(self) -> Tuple[np.array, np.array]:
        dec = self._quotes["open"] > self._quotes["close"]

        r = np.abs(self._quotes["open"] - self._quotes["close"])
        avg = (self._quotes["open"] + self._quotes["close"]) / 2.0

        mini = r < self._body_min_height

        top = np.copy(self._quotes["close"].to_numpy())
        bottom = np.copy(self._quotes["open"].to_numpy())

        top[dec] = self._quotes[dec]["open"].to_numpy()
        bottom[dec] = self._quotes[dec]["close"].to_numpy()

        top[mini] = avg[mini].to_numpy() + (self._body_min_height / 2.0)
        bottom[mini] = avg[mini].to_numpy() - (self._body_min_height / 2.0)

        return (top, bottom)

    def _plot_trading_records(
        self,
        records: List[FuturesTransaction],
        cb: Callable[[int, float, str, str, str], Any],
    ) -> None:

        table = {
            "long": "L",
            "short": "S",
            "increase": "A",
            "decrease": "D",
            "close": "X",
        }

        mn, mx = self._ylim_from_price_range()
        m = (mn + mx) / 2.0

        records.sort(key=lambda x: x.time_stamp)

        ts: Dict[int, Dict[str, Any]] = {}

        for i, t in enumerate(self._quotes.index):

            s = t
            e: datetime
            if i + 1 < len(self._quotes.index):
                e = self._quotes.index[i + 1]
            else:
                e = s + timedelta(days=365)

            assert e is not None

            for i, r in enumerate(records):
                rt = r.time

                x: Optional[int] = None
                op: Optional[str] = None
                if rt >= s and rt < e:
                    x = self._quotes.index.get_loc(s)
                    op = r.operation

                if x is None or op is None:
                    continue

                assert x is not None
                assert op is not None

                assert op in tuple(table.keys())

                t = table[op]

                h = self._quotes.iloc[x]["high"]
                l = self._quotes.iloc[x]["low"]
                pm = (h + l) / 2.0

                y = 0
                va = ""

                if pm > m:
                    y = l - self._body_min_height * 2
                    va = "top"
                else:
                    y = h + self._body_min_height * 2
                    va = "bottom"

                if x in ts:
                    ts[x]["t"].append(t)
                else:
                    ts[x] = {}
                    ts[x]["y"] = y
                    ts[x]["va"] = va
                    ts[x]["t"] = [t]

        for x, vs in ts.items():

            y = vs["y"]
            t = "\n".join(vs["t"])

            ha = "center"
            va = vs["va"]

            cb(x, y, t, ha, va)

    def _plot_indicators(self, cb: Callable[[str, str, str], Any]) -> None:
        smas = []
        bbs = []

        for col in self._quotes.columns:
            if "sma" in col:
                smas.append(col)
            elif "bb" in col:
                bbs.append(col)

        if len(smas) > 0:

            smas.sort(key=lambda x: int(x.replace("sma", "")))

            for i, col in enumerate(smas):
                cb(col, f"sma{i}", "sma")

        if len(bbs) > 0:

            bbs.sort(key=lambda x: float(re.match(r"bb\d+[+-]([0-9.]+)", x).group(1)))

            last = ""
            ci = 0
            for col in bbs:
                m = re.match(r"bb\d+[+-]([0-9.]+)", col)
                assert m is not None
                c = m.group(1)

                if last == "":
                    last = c
                else:
                    if c != last:
                        ci += 1
                        last = c

                cb(col, f"bb{ci}", "bb")

    @abstractmethod
    def futures_price(
        self,
        output: Union[str, io.BytesIO, io.StringIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def stocks_price(
        self,
        output: Union[str, io.BytesIO, io.StringIO],
        records: Optional[List[FuturesTransaction]] = None,
        interactive: bool = False,
    ) -> None:
        raise NotImplementedError
