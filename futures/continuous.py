import re
from datetime import datetime
from typing import Optional, List

import pandas as pd
from fun.data.source import (
    HOURLY,
    DAILY,
    FREQUENCY,
    MONTHLY,
    WEEKLY,
    daily_to_monthly,
    daily_to_weekly,
)

from fun.data.barchart import BarchartContractHourly

from fun.futures.contract import (
    BARCHART,
    CONTRACT_MONTHS,
    ALL_CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    # SOYBEAN_CONTRACT_MONTHS,
    # CORN_WHEAT_CONTRACT_MONTHS,
    # SILVER_COPPER_CONTRACT_MONTHS,
    contract_list,
    Contract,
)
from fun.futures.rolling import (
    LastNTradingDays,
    RATIO,
    DIFFERENCE,
    RollingMethod,
    VolumeAndOpenInterest,
    FirstOfMonth,
)
from fun.utils import colors, pretty


class ContinuousContract:
    @classmethod
    def _default_contract_months(cls, symbol: str) -> CONTRACT_MONTHS:
        months: CONTRACT_MONTHS
        if symbol in ("cl", "ng"):
            months = ALL_CONTRACT_MONTHS
        elif symbol == "gc":
            months = EVEN_CONTRACT_MONTHS
        elif symbol in ("si", "hg"):
            # months = SILVER_COPPER_CONTRACT_MONTHS
            months = CONTRACT_MONTHS("hknuz")
        elif symbol == "zs":
            # months = SOYBEAN_CONTRACT_MONTHS
            months = CONTRACT_MONTHS("fhknqux")
        elif symbol in ("zc", "zw"):
            # months = CORN_WHEAT_CONTRACT_MONTHS
            months = CONTRACT_MONTHS("hknuz")
        else:
            months = FINANCIAL_CONTRACT_MONTHS

        assert months is not None and months != ""

        return months

    @classmethod
    def _default_rolling_method(cls, symbol: str) -> RollingMethod:
        if symbol in ("cl", "ng"):
            return VolumeAndOpenInterest(
                backup=LastNTradingDays(offset=8, adjustment_method=RATIO),
                adjustment_method=RATIO,
            )
        elif symbol in ("gc", "si"):
            return VolumeAndOpenInterest(
                backup=LastNTradingDays(offset=27, adjustment_method=RATIO),
                adjustment_method=RATIO,
            )
        elif symbol in ("zs", "zc", "zw"):
            return VolumeAndOpenInterest(
                backup=LastNTradingDays(offset=15, adjustment_method=RATIO),
                adjustment_method=RATIO,
            )
        elif symbol in ("zn", "zf", "zt", "zb", "ge", "tj", "gg"):
            return VolumeAndOpenInterest(
                # backup=FirstOfMonth(adjustment_method=RATIO),
                # adjustment_method=RATIO,
                backup=FirstOfMonth(adjustment_method=DIFFERENCE),
                adjustment_method=DIFFERENCE,
            )
        elif symbol in ("e6", "j6", "b6", "a6", "d6", "s6", "n6", "dx"):
            return VolumeAndOpenInterest(
                backup=LastNTradingDays(offset=2, adjustment_method=RATIO),
                adjustment_method=RATIO,
            )
        else:
            return VolumeAndOpenInterest(
                backup=LastNTradingDays(offset=4, adjustment_method=RATIO),
                adjustment_method=RATIO,
            )
            # return LastNTradingDays(offset=4, adjustment_method=RATIO)
            # return FirstOfMonth(adjustment_method=RATIO)
            # return LastNTradingDays(offset=2, adjustment_method=RATIO)

    def _read_hourly_contract(
        self,
        start: datetime,
        end: datetime,
        symbol: str,
        frequency: FREQUENCY,
        daily_contracts: List[Contract],
        contract_months: Optional[CONTRACT_MONTHS] = None,
        rolling_method: Optional[RollingMethod] = None,
    ) -> pd.DataFrame:
        hourly_contracts = contract_list(
            start=start,
            end=end,
            symbol=symbol,
            months=contract_months,
            fmt=BARCHART,
            read_data=True,
            src=BarchartContractHourly(),
            frequency=HOURLY,
        )

        daily_length = len(daily_contracts)

        split_hour = 16

        rolling_date = rolling_method.rolling_date(
            daily_contracts[1], daily_contracts[0]
        )

        rolling_date = rolling_date.replace(hour=split_hour)

        link: pd.DataFrame
        for i in range(daily_length):
            df = hourly_contracts[i].dataframe()
            if i == 0:
                link = df.loc[df.index >= rolling_date].sort_index(ascending=False)
                continue
            else:
                part = df.loc[(df.index < rolling_date)].sort_index(ascending=False)

                columns = ["open", "high", "low", "close"]
                part.loc[:, columns] = rolling_method.adjust(part.loc[:, columns])

                link = link.loc[link.index >= rolling_date].append(part)

                if i + 1 < daily_length:
                    rolling_date = rolling_method.rolling_date(
                        daily_contracts[i + 1], daily_contracts[i]
                    )
                else:
                    p = daily_contracts[i].previous_contract(read_data=False)
                    rolling_date = datetime(
                        year=p.year(), month=p.month(), day=1, hour=split_hour
                    )
                    # p = daily_contracts[i].previous_contract(read_data=True)
                    # rolling_date = rolling_method.rolling_date(
                    # p, daily_contracts[i]
                    # )

                rolling_date = rolling_date.replace(hour=split_hour)

        link = link.loc[link.index >= rolling_date]

        assert link is not None

        link = link.sort_index()

        return link

    def read(
        self,
        start: datetime,
        end: datetime,
        symbol: str,
        frequency: FREQUENCY,
        contract_months: Optional[CONTRACT_MONTHS] = None,
        rolling_method: Optional[RollingMethod] = None,
    ) -> pd.DataFrame:

        assert re.match(r"^\w+$", symbol) is not None
        assert frequency in (HOURLY, DAILY, WEEKLY, MONTHLY)

        if contract_months is None:
            contract_months = self._default_contract_months(symbol)

        if rolling_method is None:
            rolling_method = self._default_rolling_method(symbol)

        cs = contract_list(
            start=start,
            end=end,
            symbol=symbol,
            months=contract_months,
            fmt=BARCHART,
            read_data=True,
        )

        cs_length = len(cs)

        if cs_length == 0:
            raise ValueError("empty contract list")
        elif cs_length == 1:
            return cs[0].dataframe()

        if frequency == HOURLY:
            return self._read_hourly_contract(
                start=start,
                end=end,
                symbol=symbol,
                frequency=frequency,
                daily_contracts=cs,
                contract_months=contract_months,
                rolling_method=rolling_method,
            )

        rolling_date = rolling_method.rolling_date(cs[1], cs[0])

        link: pd.DataFrame
        for i in range(cs_length):
            df = cs[i].dataframe()
            if i == 0:
                link = df.loc[df.index >= rolling_date].sort_index(ascending=False)
                continue
            else:
                part = df.loc[(df.index < rolling_date)].sort_index(ascending=False)

                columns = ["open", "high", "low", "close"]
                part.loc[:, columns] = rolling_method.adjust(part.loc[:, columns])

                link = link.loc[link.index >= rolling_date].append(part)

                if i + 1 < cs_length:
                    rolling_date = rolling_method.rolling_date(cs[i + 1], cs[i])
                else:
                    p = cs[i].previous_contract(read_data=False)
                    rolling_date = datetime(year=p.year(), month=p.month(), day=1)

        link = link.loc[link.index >= rolling_date]

        assert link is not None

        link = link.sort_index()

        if frequency == WEEKLY:
            link = daily_to_weekly(link)
        elif frequency == MONTHLY:
            link = daily_to_monthly(link)

        length = len(link)

        na = link.isna().any(axis=1)
        if na.any():
            pretty.color_print(
                colors.PAPER_AMBER_300,
                f"dropping {len(link.loc[na])} rows containing nan from {symbol.upper()}",
            )

            dropped_length = len(link.loc[na])

            link = link.dropna()

            assert length == len(link) + dropped_length

        return link


# if __name__ == "__main__":
    # start = datetime.strptime("20200101", "%Y%m%d")
    # end = datetime.strptime("20210101", "%Y%m%d")

    # src = ContinuousContract()
    # df = src.read(start=start, end=end, symbol="zn", frequency=HOURLY)
    # print(df.head(50))
