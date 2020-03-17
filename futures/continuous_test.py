import unittest
from datetime import datetime

from fun.data.source import DAILY
from fun.futures.continuous import ContinuousContract
from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    BARCHART,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    contract_list,
)
from fun.futures.rolling import NO_ADJUSTMENT, LastNTradingDays, RATIO, DIFFERENCE
from fun.utils.testing import parameterized


class TestContinuousContract(unittest.TestCase):
    # def equal_part(
    # self, df, front, back, rolling_date, columns, adjustment_back, adjustment_front
    # ):
    # self.assertTrue(
    # df.loc[(df.index >= rolling_date) & (df.index.isin(back.index)), columns]
    # .eq(
    # adjustment_back(
    # back.loc[
    # (back.index >= rolling_date) & (back.index.isin(df.index)),
    # columns,
    # ]
    # )
    # )
    # .all(axis=1)
    # .all()
    # )

    # self.assertTrue(
    # df.loc[(df.index < rolling_date) & (df.index.isin(front.index)), columns]
    # .eq(
    # adjustment_front(
    # front.loc[
    # (front.index < rolling_date) & (front.index.isin(df.index)),
    # columns,
    # ]
    # )
    # )
    # .all(axis=1)
    # .all()
    # )

    @parameterized(
        [
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": LastNTradingDays(
                    offset=4, adjustment_method=DIFFERENCE
                ),
                "rolling_date": ["20191217", "20190917", "20190618", "20190312"],
                "adjustment": [
                    lambda x: x,
                    lambda x: x + 3.5,
                    lambda x: x + 6,
                    lambda x: x + 10.5,
                    lambda x: x + 15.25,
                ],
            },
            # {
            # "start": "20200101",
            # "end": "20200101",
            # "symbol": "es",
            # "rolling_method": LastNTradingDays(
            # offset=4, adjustment_method=NO_ADJUSTMENT
            # ),
            # "adjustment": [lambda x: x, lambda x: x],
            # },
            # {
            # "start": "20200101",
            # "end": "20200101",
            # "symbol": "es",
            # "rolling_method": LastNTradingDays(
            # offset=4, adjustment_method=DIFFERENCE
            # ),
            # "adjustment": [lambda x: x, lambda x: x + (3195.5 - 3192)],
            # },
            # {
            # "start": "20191201",
            # "end": "20200101",
            # "symbol": "es",
            # "rolling_method": LastNTradingDays(
            # offset=4, adjustment_method=DIFFERENCE
            # ),
            # "adjustment": [
            # lambda x: x,
            # lambda x: x + (3195.5 - 3192),
            # lambda x: x + (3195.5 - 3192 + 3008 - 3005.5),
            # ],
            # },
            # {
            # "start": "20200101",
            # "end": "20200101",
            # "symbol": "es",
            # "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
            # "adjustment": [lambda x: x, lambda x: x * (3195.5 / 3192)],
            # },
        ]
    )
    def test_no_adjustment(
        self, start, end, symbol, rolling_method, rolling_date, adjustment
    ):
        c = ContinuousContract()

        s = datetime.strptime(start, "%Y%m%d")
        e = datetime.strptime(end, "%Y%m%d")

        df = c.read(
            start=s,
            end=e,
            symbol=symbol,
            frequency=DAILY,
            rolling_method=rolling_method,
        )

        rolling_date = [datetime.strptime(r, "%Y%m%d") for r in rolling_date]

        months = FINANCIAL_CONTRACT_MONTHS
        if symbol == "cl":
            months = ALL_CONTRACT_MONTHS
        elif symbol == "gc":
            months = EVEN_CONTRACT_MONTHS

        cs = contract_list(s, e, symbol, months, BARCHART)

        print([c.code() for c in cs])

        assert len(rolling_date) + 1 == len(adjustment)

        columns = ["open", "high", "low", "close"]

        # print(df)

        # print(df.tail(90))
        # for i in range(1, len(df.tail(120))):
        # print(df.iloc[-i])

        # i = 0
        # print(cs[i].code())
        # cdf = cs[i].dataframe()

        # print(
        # df.loc[(df.index >= rolling_date[i]) & (df.index.isin(cdf.index)), columns,]
        # )

        # print(
        # adjustment[i](
        # cdf.loc[
        # (cdf.index >= rolling_date[i]) & (cdf.index.isin(df.index)),
        # columns,
        # ]
        # )
        # )

        # i = 1
        # # print(cs[i].code())
        # cdf = cs[i].dataframe()

        # print(
        # df.loc[
        # (df.index < rolling_date[i - 1])
        # & (df.index >= rolling_date[i])
        # & (df.index.isin(cdf.index)),
        # columns,
        # ]
        # )

        # print(
        # adjustment[i](
        # cdf.loc[
        # (cdf.index < rolling_date[i - 1])
        # & (cdf.index >= rolling_date[i])
        # & (cdf.index.isin(df.index)),
        # columns,
        # ]
        # )
        # )

        # print(df.loc[
        # (df.index < rolling_date[0])
        # & (df.index >= rolling_date[1])
        # & (df.index.isin(cs[1].dataframe().index)),
        # columns,
        # ])

        for i in range(len(rolling_date)):
            if i < len(rolling_date) - 1:
                cdf = cs[i].dataframe()
                print(
                    df.loc[
                        (df.index >= rolling_date[i]) & (df.index.isin(cdf.index)),
                        columns,
                    ]
                )
                print(
                    adjustment[i](
                        cdf.loc[
                            (cdf.index >= rolling_date[i]) & (cdf.index.isin(df.index)),
                            columns,
                        ]
                    )
                )
                print(
                    df.loc[(df.index >= rolling_date[i]) & (df.index.isin(cdf.index))]
                    .eq(
                        adjustment[i](
                            cdf.loc[
                                (cdf.index >= rolling_date[i])
                                & (cdf.index.isin(df.index))
                            ]
                        )
                    )
                    .all(axis=1)
                    .all()
                )

            if i > 1:
                break

    # df.loc[(df.index < rolling_date) & (df.index.isin(front.index)), columns]
    # .eq(
    # adjustment_front(
    # front.loc[
    # (front.index < rolling_date) & (front.index.isin(df.index)),
    # columns,
    # ]
    # )

    # print([c.code() for c in cs])

    # assert len(cs) >= 2
    # assert len(adjustment) == len(cs)

    # for i in range(len(cs) - 1):
    # back = cs[i]
    # front = cs[i + 1]

    # rolling_date = rolling_method.rolling_date(front, back)

    # print(rolling_date)

    # # columns = ["open", "high", "low", "close"]
    # # self.equal_part(
    # # df,
    # # front.dataframe(),
    # # back.dataframe(),
    # # rolling_date,
    # # columns,
    # # adjustment[i],
    # # adjustment[i + 1],
    # # )

    # print(i)
    # print(
    # cs[len(cs) - 1]
    # .dataframe()
    # .loc[
    # # (cs[len(cs) - 1].dataframe().index.isin(back.dataframe().index))
    # (cs[len(cs) - 1].dataframe().index.isin(df.index))
    # ]
    # )
    # print(
    # front.dataframe().loc[
    # (front.dataframe().index.isin(back.dataframe().index))
    # & (front.dataframe().index.isin(df.index))
    # ]
    # )
    # print(
    # back.dataframe().loc[
    # (back.dataframe().index.isin(front.dataframe().index))
    # & (back.dataframe().index.isin(df.index))
    # ]
    # )
    # print(
    # df.loc[
    # (df.index.isin(front.dataframe().index))
    # & (df.index.isin(back.dataframe().index))
    # ]
    # )

    # columns = ["volume", "open interest"]
    # self.equal_part(
    # df,
    # front.dataframe(),
    # back.dataframe(),
    # rolling_date,
    # columns,
    # lambda x: x,
    # lambda x: x,
    # )


if __name__ == "__main__":
    unittest.main()
