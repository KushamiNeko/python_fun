import os
from datetime import datetime

import pandas as pd

from fun.data.barchart import Barchart


class Contract(Barchart):
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        return os.path.join("continuous", symbol[:2], f"{symbol}.csv",)


class ContinuousContract(Contract):
    pass


if __name__ == "__main__":
    time_fmt = "%Y%m%d"

    c = Contract()

    s = datetime.strptime("20170101", time_fmt)
    e = datetime.strptime("20180101", time_fmt)

    # contract = "clf98"
    contract = "qrh06"
    # contract = "esh20"

    df = c.read(s, e, contract, "d")

    print(df.head(15))
