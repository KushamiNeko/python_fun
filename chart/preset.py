import io
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, cast, Any

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

    def quote(self) -> Dict[str, Any]:
        df = self._cache.quotes().iloc[-1]
        return {
            "date": self._cache.quotes().index[-1].strftime("%Y%m%d"),
            "open": df.get("open"),
            "high": df.get("high"),
            "low": df.get("low"),
            "close": df.get("close"),
            "volume": df.get("volume", 0),
            "interest": df.get("open interest", 0),
        }

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

    # def inspect(self, x: float, y: float, decimals: int=2) -> Optional[Tuple[datetime, float]]:
    def inspect(
        self,
        x: float,
        y: float,
        ax: Optional[float] = None,
        ay: Optional[float] = None,
        decimals: int = 2,
    ) -> Optional[Dict[str, str]]:
        n = self._cache.chart().to_data_coordinates(x, y)
        if n is None:
            return None

        nx, ny = n

        df = self._cache.quotes()

        info = {
            "date": self._cache.quotes().index[nx].strftime("%Y-%m-%d"),
            "price": f"{ny:,.{decimals}f}",
            "open": f"{df.iloc[nx].get('open'):,.{decimals}f}",
            "high": f"{df.iloc[nx].get('high'):,.{decimals}f}",
            "low": f"{df.iloc[nx].get('low'):,.{decimals}f}",
            "close": f"{df.iloc[nx].get('close'):,.{decimals}f}",
            "volume": f"{df.iloc[nx].get('volume', 0):,.0f}",
            "interest": f"{df.iloc[nx].get('open interest', 0):,.0f}",
        }

        if ax is None or ay is None:
            if nx != 0:
                base = self._cache.quotes().iloc[nx - 1].get("close")
                info["diff($)"] = f"{df.iloc[nx].get('close') - base:,.{decimals}f}"

                info[
                    "diff(%)"
                ] = f"{((df.iloc[nx].get('close') - base) / base) * 100.0:,.{decimals}f}"

        else:
            an = self._cache.chart().to_data_coordinates(ax, ay)
            assert an is not None

            ax, ay = an

            base_date = self._cache.quotes().index[ax]

            print(ax, ay)
            print(base_date)
            print(df.index[nx])

            info["diff(d)"] = f"{(df.index[nx] - base_date).days}"
            info["diff(w)"] = f"{(df.index[nx] - base_date).days // 7}"
            info["diff($)"] = f"{ny - ay:,.{decimals}f}"
            info["diff(%)"] = f"{((ny - ay) / ay) * 100.0:,.{decimals}f}"

        return info
