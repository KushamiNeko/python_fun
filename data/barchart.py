import os
import re
from datetime import datetime

import pandas as pd

from fun.utils import colors, pretty
from source import DataSource


class BarchartOnDemand(DataSource):
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

    def _timestamp_preprocessing(self, x: str) -> datetime:
        m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})-\d{2}:\d{2}", x)
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


class Barchart(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:

        # barchart historic
        m = re.match(r"^\d{2}/\d{2}/\d{4}$", x)
        if m is not None:
            return datetime.strptime(x, r"%m/%d/%Y")

        # barchart interactive
        m = re.match(r"^\d{4}-\d{2}-\d{2}$", x)
        if m is not None:
            return datetime.strptime(x, r"%Y-%m-%d")

        # barchart ondemand
        m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})-\d{2}:\d{2}$", x)
        if m is not None:
            return datetime.strptime(m.group(1), r"%Y-%m-%dT%H:%M:%S")

        raise ValueError("unknown timestamp format")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: str
    ) -> pd.DataFrame:

        df = pd.read_csv(self._path("barchart", symbol, ext="csv"))

        na = df[df.isna().any(axis=1)]

        pretty.color_print(
            colors.PAPER_RED_400, f"dropping row containing nan\n{na}",
        )

        df = df.drop(na.index)

        return df

    # def read(
    # self, start: datetime, end: datetime, symbol: str, frequency: str
    # ) -> pd.DataFrame:

    # df = super().read(start, end, symbol, frequency)

    # return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        # barchart historic
        if "Time" in df.columns:
            cols["Time"] = "timestamp"
        # barchart interactive
        elif "Date Time" in df.columns:
            cols["Date Time"] = "timestamp"

        return df.rename(columns=cols)


if __name__ == "__main__":
    time_fmt = "%Y%m%d"

    c = Barchart()

    s = datetime.strptime("20170101", time_fmt)
    e = datetime.strptime("20180101", time_fmt)

    df = c.read(s, e, "spx", "d")

    print(df)
