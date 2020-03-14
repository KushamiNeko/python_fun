import os
from datetime import datetime

import pandas as pd

from fun.data.barchart import Barchart


class Contract(Barchart):
    def _url(self, start: datetime, end: datetime, symbol: str, frequency: str) -> str:
        return os.path.join("continuous", symbol[:2], f"{symbol}.csv",)


class ContinuousContract(Contract):
    pass
