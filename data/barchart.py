import os
import re
from datetime import datetime, timedelta

import pandas as pd
from fun.data.source import DAILY, DataSource, FREQUENCY, HOURLY, MONTHLY, WEEKLY


class BarchartOnDemand(DataSource):
    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:

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

    def _interval(self, freq: FREQUENCY) -> str:
        if freq == HOURLY:
            return "60"
        else:
            return "1"

    def _frequency(self, freq: FREQUENCY) -> str:
        if freq == HOURLY:
            return "nearbyMinutes"
        elif freq == DAILY:
            return "dailyNearest"
        elif freq == WEEKLY:
            return "weeklyNearest"
        elif freq == MONTHLY:
            return "monthlyNearest"
        else:
            raise ValueError(f"invalid frequency: {freq}")

    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:

        df = pd.read_csv(self._datafeed(self._url(start, end, symbol, DAILY)))
        return df


class Barchart(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:

        # barchart historic
        if re.match(r"^\d{2}/\d{2}/\d{4}$", x) is not None:
            return datetime.strptime(x, r"%m/%d/%Y")

        if re.match(r"^\d{2}/\d{2}/\d{2}$", x) is not None:
            return datetime.strptime(x, r"%m/%d/%y")

        # barchart historic hourly
        if re.match(r"^\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}$", x) is not None:
            return datetime.strptime(x, r"%m/%d/%Y %H:%M")

        # barchart interactive
        if re.match(r"^\d{4}-\d{2}-\d{2}$", x) is not None:
            return datetime.strptime(x, r"%Y-%m-%d")

        # barchart interactive hourly
        if re.match(r"^\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}$", x) is not None:
            return datetime.strptime(x, r"%Y-%m-%d %H:%M:%S")

        # barchart ondemand
        m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})-\d{2}:\d{2}$", x)
        if m is not None:
            return datetime.strptime(m.group(1), r"%Y-%m-%dT%H:%M:%S")

        raise ValueError(f"unknown timestamp format: {x}")

    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        return os.path.join("barchart", f"{symbol}.csv")

    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:

        with open(self._localfile(self._url(start, end, symbol, DAILY)), "r") as f:
            content = f.readlines()

        if (
            # re.match(
                # r"""["']*Symbol:\s*\w+\d*["']*,+["']*Study:\s*\w+["']*,""",
                # content[0].strip(),
            # )
            # is not None
            "Study:" in content[0].strip() and "Symbol:" in content[0].strip()
        ):
            df = pd.read_csv(
                self._localfile(self._url(start, end, symbol, DAILY)), header=1
            )
        else:
            df = pd.read_csv(self._localfile(self._url(start, end, symbol, DAILY)))

        if (
            re.match(
                r"""["']*\s*Downloaded\s*from\s*Barchart\.com\s*as\s*of\s*\d{2}-\d{2}-\d{4}\s*\d{2}:\d{2}[ap]m\s*C[SD]T["']*""",
                content[-1].strip(),
            )
            is not None
        ):
            df = df.drop(df.tail(1).index)

        df = df.fillna(0)

        columns = df.columns

        # barchart historic
        if "Change" in columns:
            df = df.drop("Change", axis=1)

        if "%Chg" in columns:
            df = df.drop("%Chg", axis=1)

        # barchart ondemand
        if "symbol" in columns:
            df = df.drop("symbol", axis=1)

        if "tradingDay" in columns:
            df = df.drop("tradingDay", axis=1)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}

        columns = df.columns

        # barchart historic
        if "Time" in columns:
            cols["Time"] = "timestamp"

        if "Open Int" in columns:
            cols["Open Int"] = "open interest"

        if "Last" in columns:
            cols["Last"] = "close"

        # barchart interactive
        if "Date Time" in columns:
            cols["Date Time"] = "timestamp"

        # barchart ondemand
        if "openInterest" in columns:
            cols["openInterest"] = "open interest"

        return df.rename(columns=cols)


class BarchartContract(Barchart):
    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        return os.path.join(
            "continuous",
            symbol[:2],
            f"{symbol}.csv",
        )


class BarchartContractHourly(Barchart):
    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:

        return os.path.join(
            "continuous",
            f"{symbol[:2]}@h",
            f"{symbol}.csv",
        )


#    def _timestamp_preprocessing(self, x: str) -> datetime:
#        m = re.match(r"^\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}$", x)
#        assert m is not None
#
#        dt = datetime.strptime(x, r"%Y-%m-%d %H:%M:%S")
#        # dt += timedelta(hours=1)
#
#        return dt
#
#    def _read_data(self, start: datetime, end: datetime, symbol: str) -> pd.DataFrame:
#
#        path = self._localfile(
#            self._url(start=start, end=end, symbol=symbol, frequency=HOURLY)
#        )
#
#        df = pd.read_csv(path, header=1)
#        df = df.drop(df.tail(1).index)
#        df = df.drop("Change", axis=1)
#        df.loc[:, "Open Interest"] = df.loc[:, "Open Interest"].fillna(0)
#
#        return df
#
#    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
#        cols = {k: k.lower() for k in df.columns}
#        cols["Date Time"] = "timestamp"
#        return df.rename(columns=cols)


# if __name__ == "__main__":
# start = datetime.strptime("20200101", "%Y%m%d")
# end = datetime.strptime("20210101", "%Y%m%d")

# src = BarchartContractHourly()
# # df = src._read_data(start=start, end=end, symbol="znz20")
# df = src.read(start=start, end=end, symbol="znz20", frequency=HOURLY)
# print(df.tail(25))
