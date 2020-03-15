from datetime import datetime

import pandas as pd

from fun.data.barchart import BarchartContract
from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
)
from fun.futures.contract import contract_list


class ContinuousContract(BarchartContract):
    def _contract_months(self, symbol: str) -> str:
        if symbol in ["cl"]:
            return ALL_CONTRACT_MONTHS
        elif symbol in ["gc"]:
            return EVEN_CONTRACT_MONTHS
        else:
            return FINANCIAL_CONTRACT_MONTHS

    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: str
    ) -> pd.DataFrame:

        contract_list = contract_list(
            start=start,
            end=end,
            symbol=symbol,
            months=self._contract_months(symbol),
            fmt="barchart",
            read_data=True,
        )
