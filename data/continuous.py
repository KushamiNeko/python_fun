import os
import re
from datetime import datetime

import pandas as pd
from fun.utils import colors, pretty
from source import DataSource
from barchart import Barchart


class ContinuousContract(Barchart):
    def _localpath(self, folder: str, contract: str, ext: str = "csv") -> str:

        home = os.getenv("HOME")
        assert home is not None

        path = os.path.join(
            home,
            "Documents",
            "data_source",
            "continuous",
            contract[:2],
            f"{contract}.{ext}",
        )
        if not os.path.exists(path):
            pretty.color_print(colors.PAPER_RED_400, f"unknown path: {path}")
            raise ValueError(f"unknown contract: {contract}")

        assert os.path.exists(path)

        return path


if __name__ == "__main__":
    time_fmt = "%Y%m%d"

    c = ContinuousContract()

    s = datetime.strptime("20170101", time_fmt)
    e = datetime.strptime("20180101", time_fmt)

    contract = "clf98"
    # contract = "qrh03"

    df = c.read(s, e, contract, "d")

    print(df.tail(15))

    df = c.read(s, e, contract, "w")

    print(df.tail(15))
