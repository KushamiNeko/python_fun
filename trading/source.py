import io
import os
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests


class DataSource(metaclass=ABCMeta):
    @abstractmethod
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def _index_preprocessor(self, x: str) -> datetime:
        raise NotImplementedError

    def _preload(self, freq: str) -> timedelta:
        preload = 30

        if freq in ("h", "hourly"):
            return timedelta(hours=preload * 3)
        elif freq in ("d", "daily"):
            return timedelta(days=preload)
        elif freq in ("w", "weekly"):
            return timedelta(weeks=preload)
        elif freq in ("m", "monthly"):
            return timedelta(days=preload * 31)
        else:
            raise ValueError(f"invalid frequency: {freq}")

    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: str
    ) -> pd.DataFrame:

        if frequency not in (
            "h",
            "d",
            "w",
            "m",
            "hourly",
            "daily",
            "weekly",
            "monthly",
        ):
            raise ValueError(f"invalid frequency: {frequency}")

        url = self._url(start, end, symbol, frequency)

        resp = requests.get(url)
        resp.raise_for_status()

        data = io.BytesIO(resp.content)
        df = pd.read_csv(data)

        cols = {k: k.lower() for k in df.columns}
        df = df.rename(columns=cols)

        df["timestamp"] = df["timestamp"].apply(self._index_preprocessor)
        df = df.set_index("timestamp")

        return df


class Barchart(DataSource):
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:

        if not re.match(r"^[a-zA-Z]+[0-9]{2}$", symbol):
            raise ValueError(f"invalid symbol: {symbol}")

        if os.getenv("BARCHART") is None:
            raise ValueError("empty BARCHART environment variable")

        time_fmt = "%Y%m%d"

        root = r"https://ondemand.websol.barchart.com/getHistory.csv"

        queries = [
            f"apikey={os.getenv('BARCHART', '')}",
            f"symbol={symbol}",
            f"type={self._frequency(frequency)}",
            f"startDate={(start - self._preload(frequency)).strftime(time_fmt)}",
            f"endDate={end.strftime(time_fmt)}",
            f"interval={self._interval(frequency)}",
            "volume=total",
            "backAdjust=true",
            "contractRoll=combined",
        ]

        url = f"{root}?{'&'.join(queries)}"

        return url

    def _index_preprocessor(self, x: str) -> datetime:
        pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})-\d{2}:\d{2}"

        m = re.match(pattern, x)
        assert m is not None

        return datetime.strptime(m.group(1), r"%Y-%m-%dT%H:%M:%S")

    def _interval(self, freq: str) -> str:
        if freq in ("h", "hourly"):
            return "60"
        else:
            return "1"

    def _frequency(self, freq: str) -> str:
        if freq in ("h", "hourly"):
            return "nearbyMinutes"
        elif freq in ("d", "daily"):
            return "dailyNearest"
        elif freq in ("w", "weekly"):
            return "weeklyNearest"
        elif freq in ("m", "monthly"):
            return "monthlyNearest"
        else:
            raise ValueError(f"invalid frequency: {freq}")


class AlphaVantage(DataSource):
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:

        if not re.match(r"^[a-zA-Z]+$", symbol):
            raise ValueError(f"invalid symbol: {symbol}")

        if os.getenv("ALPHA_VANTAGE") is None:
            raise ValueError("empty ALPHA_VANTAGE environment variable")

        root = r"https://www.alphavantage.co/query"

        queries = [
            f"apikey={os.getenv('ALPHA_VANTAGE', '')}",
            f"symbol={symbol}",
            f"function={self._frequency(frequency)}",
            "interval=60min",
            "outputsize=full",
            "datatype=csv",
        ]

        url = f"{root}?{'&'.join(queries)}"
        return url

    def _index_preprocessor(self, x: str) -> datetime:
        pattern = r"^\d{4}-\d{2}-\d{2}$"

        if re.match(pattern, x):
            return datetime.strptime(x, "%Y-%m-%d")
        else:
            return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

    def _frequency(self, freq: str) -> str:
        if freq in ("h", "hourly"):
            return "TIME_SERIES_INTRADAY"
        elif freq in ("d", "daily"):
            return "TIME_SERIES_DAILY"
        elif freq in ("w", "weekly"):
            return "TIME_SERIES_WEEKLY"
        elif freq in ("m", "monthly"):
            return "TIME_SERIES_MONTHLY"
        else:
            raise ValueError(f"invalid frequency: {freq}")

    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: str
    ) -> pd.DataFrame:

        df = super().read(start, end, symbol, frequency)
        df = df.iloc[::-1]

        return df


class Yahoo:
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        pass

    def _index_preprocessor(self, x: str) -> datetime:
        return datetime.strptime(x, "%Y-%m-%d").astimezone(
            timezone(timedelta(hours=-5))
        )

    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: str
    ) -> pd.DataFrame:

        if frequency not in (
            "h",
            "d",
            "w",
            "m",
            "hourly",
            "daily",
            "weekly",
            "monthly",
        ):
            raise ValueError(f"invalid frequency: {frequency}")

        home = os.getenv("HOME")
        assert home is not None

        path = os.path.join(
            home, "Documents", "data_source", "yahoo", f"{symbol}_{frequency[0]}.csv"
        )
        if not os.path.exists(path):
            print(path)
            raise ValueError(f"unknown symbol: {symbol}")

        assert os.path.exists(path)

        df = pd.read_csv(path)

        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        df = df.rename(columns=cols)

        df["timestamp"] = df["timestamp"].apply(self._index_preprocessor)
        df = df.set_index("timestamp")

        return df


if __name__ == "__main__":
    time_fmt = "%Y%m%d"

    c = Barchart()
    # c = AlphaVantage()

    s = datetime.strptime("20170101", time_fmt)
    e = datetime.strptime("20180101", time_fmt)

    df = c.read(s, e, "znz19", "d")
    # df = c.read(s, e, "spx", "d")

    print(df)
