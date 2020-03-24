import io
import re
from datetime import datetime, timedelta
from typing import List, Optional, cast, Tuple

import pandas as pd

from fun.chart.base import MEDIUM_CHART, SMALL_CHART
from fun.chart.cache import QuotesCache
from fun.chart.static import CandleSticks
from fun.data.source import (
    DAILY,
    FREQUENCY,
    HOURLY,
    MONTHLY,
    WEEKLY,
    DataSource,
    InvestingCom,
    StockCharts,
    Yahoo,
)
from fun.futures.continuous import ContinuousContract
from fun.futures.rolling import RATIO, LastNTradingDays, VolumeAndOpenInterest
from fun.trading.transaction import FuturesTransaction


class ChartPreset:
    def __init__(self, dtime: datetime, symbol: str, frequency: FREQUENCY) -> None:
        assert re.match(r"^[a-zA-Z0-9]+$", symbol) is not None

        self._symbol = symbol

        assert frequency in (DAILY, WEEKLY)

        self._frequency = frequency

        self._stime, self._etime = self._time_range(dtime)
        self._exstime, self._exetime = self._extime_range()

        self._frequency = frequency

        self._cache = self._read_chart_data()

    def _time_range(self, dtime: datetime) -> Tuple[datetime, datetime]:

        etime = dtime
        stime: datetime

        if self._frequency == HOURLY:
            stime = etime - timedelta(days=15)
        elif self._frequency == DAILY:
            stime = etime - timedelta(days=365)
        elif self._frequency == WEEKLY:
            stime = etime - timedelta(days=365 * 4)
        elif self._frequency == MONTHLY:
            stime = etime - timedelta(days=368 * 18)
        else:
            raise ValueError(f"invalid frequency")

        return stime, etime

    def _extime_range(self) -> Tuple[datetime, datetime]:
        exetime = self._etime + timedelta(days=500)
        exstime = self._stime - timedelta(days=500)

        now = datetime.now()
        if exetime > now:
            exetime = now

        return exstime, exetime

    def _read_chart_data(self) -> QuotesCache:
        print("network")

        src: Optional[DataSource] = None
        # factory = lambda quotes: CandleSticks(quotes, chart_size=SMALL_CHART)
        factory = lambda quotes: CandleSticks(quotes, chart_size=MEDIUM_CHART)

        if self._symbol in ("vix", "vxn", "sml", "ovx", "gvz"):
            src = Yahoo()

        elif self._symbol in ("vstx", "jniv"):
            src = InvestingCom()

        elif self._symbol in (
            "gsy",
            "near",
            "icsh",
            "shv",
            "hyg",
            "ushy",
            "shyg",
            "emb",
            "lqd",
            "igsb",
            "igib",
            "shy",
            "iei",
            "ief",
            "govt",
            "iyr",
            "reet",
            "rem",
        ):
            src = InvestingCom()

        elif self._symbol in ("vle", "rvx", "tyvix"):
            src = StockCharts()

        df: pd.DataFrame
        if src is None:
            df = ContinuousContract().read(
                start=self._exstime,
                end=self._exetime,
                symbol=self._symbol,
                frequency=self._frequency,
                rolling_method=LastNTradingDays(offset=4, adjustment_method=RATIO),
            )
            print(df)
        else:
            df = src.read(
                start=self._exstime,
                end=self._exetime,
                symbol=self._symbol,
                frequency=self._frequency,
            )

        assert df is not None

        cache = QuotesCache(df, self._stime, self._etime, chart_factory=factory)
        return cache

    def _read_records(self) -> Optional[List[FuturesTransaction]]:
        return None

    # def time_slice(self, stime: datetime, etime: datetime) -> None:
    def time_slice(self, dtime: datetime) -> None:
        stime, etime = self._time_range(dtime)
        self._cache.time_slice(stime, etime)

    def stime(self) -> datetime:
        return cast(datetime, self._cache.stime().to_pydatetime())

    def etime(self) -> datetime:
        return cast(datetime, self._cache.etime().to_pydatetime())

    def exstime(self) -> datetime:
        # return cast(pd.Timestamp, self._quotes.index[0])
        return cast(datetime, self._cache.exstime().to_pydatetime())

    def exetime(self) -> datetime:
        # return cast(pd.Timestamp, self._quotes.index[-1])
        return cast(datetime, self._cache.exetime().to_pydatetime())

    def forward(self) -> bool:
        chart = self._cache.forward()
        if chart is None:
            return False
        else:
            return True

    def backward(self) -> bool:
        chart = self._cache.backward()
        if chart is None:
            return False
        else:
            return True

    def render(self) -> io.BytesIO:
        buf = io.BytesIO()
        self._cache.chart().plot(buf, records=self._read_records())
        buf.seek(0)

        return buf
