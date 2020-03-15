import unittest
from datetime import datetime

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    Contract,
    contract_list,
)
from fun.utils.testing import parameterized


class TestContract(unittest.TestCase):
    @parameterized(
        [
            {
                "code": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_error": ValueError,
            },
            {
                "code": "nk225m",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "quandl",
                "expect_error": ValueError,
            },
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_error": ValueError,
            },
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "quandl",
                "expect_error": ValueError,
            },
            {
                "code": "esh20",
                "months": "hello",
                "fmt": "barchart",
                "expect_error": AssertionError,
            },
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "hello",
                "expect_error": AssertionError,
            },
        ]
    )
    def test_error(self, code, months, fmt, expect_error):
        with self.assertRaises(expect_error):
            Contract(
                code=code, months=months, fmt=fmt, read_data=False,
            )

    def test_read_data(self):
        c = Contract.front_month(
            symbol="es",
            months=FINANCIAL_CONTRACT_MONTHS,
            fmt="barchart",
            read_data=False,
        ).previous_contract(read_data=True)

        self.assertNotEqual(len(c.dataframe()), 0)
        self.assertFalse(c.dataframe().isna().any(axis=1).any())
        self.assertFalse((c.dataframe().index.hour != 0).any())

    @parameterized(
        [
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_year": 2020,
                "expect_month": 3,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esz19",
            },
            {
                "code": "esu99",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_year": 1999,
                "expect_month": 9,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esm99",
            },
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "quandl",
                "expect_year": 1999,
                "expect_month": 6,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mh1999",
            },
            {
                "code": "nk225mu2019",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "quandl",
                "expect_year": 2019,
                "expect_month": 9,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mm2019",
            },
            {
                "code": "clf19",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_year": 2019,
                "expect_month": 1,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clz18",
            },
        ]
    )
    def test_contract(
        self,
        code,
        months,
        fmt,
        expect_year,
        expect_month,
        expect_symbol,
        expect_previous_contract_code,
    ):
        c = Contract(code=code, months=months, fmt=fmt, read_data=False)

        self.assertEqual(c.year(), expect_year)
        self.assertEqual(c.month(), expect_month)
        self.assertEqual(c.symbol(), expect_symbol)

        self.assertEqual(
            c.previous_contract(read_data=False).code(), expect_previous_contract_code
        )

    @parameterized(
        [
            {
                "time": "20181205",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "esh19",
            },
            {
                "time": "20080201",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "esm08",
            },
            {
                "time": "20181005",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "esz18",
            },
            {
                "time": "19991005",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "esz99",
            },
            {
                "time": "20180105",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "esh18",
            },
            {
                "time": "20180605",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "esu18",
            },
            {
                "time": "20180605",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "clu18",
            },
            {
                "time": "20181206",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "clh19",
            },
            {
                "time": "20081206",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "clh09",
            },
            {
                "time": "20180805",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "clx18",
            },
            {
                "time": "20180406",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "cln18",
            },
            {
                "time": "20180605",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "gcv18",
            },
            {
                "time": "20180305",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "gcm18",
            },
            {
                "time": "20000305",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "gcm00",
            },
            {
                "time": "20180205",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "gcm18",
            },
            {
                "time": "20181206",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "gcj19",
            },
            {
                "time": "20181106",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_code": "gcg19",
            },
        ]
    )
    def test_front_month(self, time, symbol, months, fmt, expect_code):
        c = Contract.front_month(
            symbol=symbol,
            months=months,
            fmt=fmt,
            time=datetime.strptime(time, "%Y%m%d"),
            read_data=False,
        )
        self.assertEqual(c.code(), expect_code)

    @parameterized(
        [
            {
                "start": "20170905",
                "end": "20181205",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_list": "esh19,esz18,esu18,esm18,esh18,esz17,esu17,esm17",
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_list": "esh19,esz18,esu18,esm18,esh18,esz17,esu17",
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_list": "gcj19,gcg19,gcz18,gcv18,gcq18,gcm18,gcj18,gcg18,gcz17,gcv17",
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": "barchart",
                "expect_list": "clj19,clh19,clg19,clf19,clz18,clx18,clv18,clu18,clq18,cln18,clm18,clk18,clj18,clh18,clg18,clf18,clz17,clx17",
            },
        ]
    )
    def test_contract_list(self, start, end, symbol, months, fmt, expect_list):
        cs = contract_list(
            start=datetime.strptime(start, "%Y%m%d"),
            end=datetime.strptime(end, "%Y%m%d"),
            symbol=symbol,
            months=months,
            fmt=fmt,
            read_data=False,
        )
        self.assertListEqual([c.code() for c in cs], expect_list.split(","))


if __name__ == "__main__":
    unittest.main()
