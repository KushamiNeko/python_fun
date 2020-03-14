import io
import os
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests

from fun.utils import colors, pretty


class DataSource(metaclass=ABCMeta):
    @abstractmethod
    def _timestamp_preprocessing(self, x: str) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        raise NotImplementedError

    def _datafeed(self, url: str) -> io.BytesIO:
        resp = requests.get(url)
        resp.raise_for_status()

        data = io.BytesIO(resp.content)

        return data

    def _localfile(self, path: str) -> str:

        home = os.getenv("HOME")
        assert home is not None

        path = os.path.join(home, "Documents", "data_source", path)
        if not os.path.exists(path):
            pretty.color_print(colors.PAPER_RED_400, f"unknown path: {path}")
            raise ValueError(f"unknown path: {path}")

        return path

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

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        return df.rename(columns=cols)

    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: str
    ) -> pd.DataFrame:

        assert frequency in ("d", "w")

        df = self._read_data(start, end, symbol)

        df = self._rename_columns(df)

        df.loc[:, "timestamp"] = df.loc[:, "timestamp"].apply(
            self._timestamp_preprocessing
        )

        df = df.set_index("timestamp")

        unusual = df.index.hour != 0
        if unusual.any():
            pretty.color_print(
                colors.PAPER_RED_400,
                f"dropping {len(df.loc[unusual])} rows containing unusual timestamp from {symbol.upper()}",
            )
            df = df.drop(df.loc[unusual].index)

        df = df.sort_index()

        # cols = ["open", "high", "low", "close", "volume"]
        # if "open interest" in df.columns:
        # cols.append("open interest")

        # df = df.loc[:, cols]

        na = df.isna().any(axis=1)
        if na.any():
            pretty.color_print(
                colors.PAPER_RED_400,
                f"dropping {len(df.loc[na])} rows containing nan from {symbol.upper()}",
            )

            df = df.dropna()

        if frequency == "w":
            agg = {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }

            if "open interest" in df.columns:
                agg["open interest"] = "sum"

            dfg = df.groupby(pd.Grouper(freq="W-MON", label="left", closed="left"))

            df = dfg.agg(agg)
            # df = dfg.agg(agg).loc[df.columns]

        return df.astype(np.float)


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

    def _timestamp_preprocessing(self, x: str) -> datetime:
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

    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:

        df = pd.read_csv(self._datafeed(self._url(start, end, symbol, "d")))
        return df


class Yahoo(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        return datetime.strptime(x, "%Y-%m-%d")

    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        return os.path.join("yahoo", f"{symbol}.csv")

    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:
        df = pd.read_csv(self._localfile(self._url(start, end, symbol, "d")))
        df = df.drop("Adj Close", axis=1)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        return df.rename(columns=cols)


class StockCharts(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        return datetime.strptime(x, "%m-%d-%Y")

    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        return os.path.join("stockcharts", f"{symbol}.txt")

    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:

        with open(self._localfile(self._url(start, end, symbol, "d")), "r") as f:
            lines = f.readlines()

        content = "\n".join([re.subn(r"\s+", ",", l.strip())[0] for l in lines])
        data = io.StringIO(content)

        df = pd.read_csv(data)

        df = df.drop(0)
        df = df.drop("Day", axis=1)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        return df.rename(columns=cols)


class InvestingCom(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        return datetime.strptime(x, "%b %d, %Y")

    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        return os.path.join("investing.com", f"{symbol}.csv")

    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:

        df = pd.read_csv(self._localfile(self._url(start, end, symbol, "d")))
        df = df.drop("Change %", axis=1)

        df.loc[:, "Vol."] = df.loc[:, "Vol."].apply(
            lambda x: 0 if x == "-" or type(x) is str else x
        )

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        cols["Vol."] = "volume"
        cols["Price"] = "close"
        return df.rename(columns=cols)
