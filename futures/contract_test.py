import unittest
from datetime import datetime

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    BARCHART,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    QUANDL,
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
                "fmt": BARCHART,
                "expect_error": ValueError,
            },
            {
                "code": "nk225m",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_error": ValueError,
            },
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_error": ValueError,
            },
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_error": ValueError,
            },
            {
                "code": "esh20",
                "months": "hello",
                "fmt": BARCHART,
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
            fmt=BARCHART,
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
                "fmt": BARCHART,
                "expect_year": 2020,
                "expect_month": 3,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esz19",
            },
            {
                "code": "esu99",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 1999,
                "expect_month": 9,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esm99",
            },
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 1999,
                "expect_month": 6,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mh1999",
            },
            {
                "code": "nk225mu2019",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 2019,
                "expect_month": 9,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mm2019",
            },
            {
                "code": "clf19",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
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
                "time": "20180105",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esh18",
            },
            {
                "time": "20080201",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esh08",
            },
            {
                "time": "19980321",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esm98",
            },
            {
                "time": "20100411",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esm10",
            },
            {
                "time": "20000529",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esm00",
            },
            {
                "time": "20180605",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esu18",
            },
            {
                "time": "19990705",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esu99",
            },
            {
                "time": "20190802",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esu19",
            },
            {
                "time": "20010923",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esz01",
            },
            {
                "time": "20181005",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esz18",
            },
            {
                "time": "20181119",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esz18",
            },
            {
                "time": "20181205",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esh19",
            },
            {
                "time": "19980119",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clj98",
            },
            {
                "time": "20000227",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clk00",
            },
            {
                "time": "20010327",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clm01",
            },
            {
                "time": "19990406",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "cln99",
            },
            {
                "time": "20100530",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clq10",
            },
            {
                "time": "20180605",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clu18",
            },
            {
                "time": "20180731",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clv18",
            },
            {
                "time": "20180805",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clx18",
            },
            {
                "time": "20110917",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clz11",
            },
            {
                "time": "19991023",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clf00",
            },
            {
                "time": "20081106",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clg09",
            },
            {
                "time": "20181206",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "clh19",
            },
            {
                "time": "19980117",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcj98",
            },
            {
                "time": "20180215",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcm18",
            },
            {
                "time": "20180305",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcm18",
            },
            {
                "time": "20000425",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcq00",
            },
            {
                "time": "20010527",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcq01",
            },
            {
                "time": "20180605",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcv18",
            },
            {
                "time": "20030731",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcv03",
            },
            {
                "time": "20050831",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcz05",
            },
            {
                "time": "20130913",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcz13",
            },
            {
                "time": "19981025",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcg99",
            },
            {
                "time": "19991106",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcg00",
            },
            {
                "time": "20181206",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "gcj19",
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
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh20,esz19,esu19,esm19,esh19,esz18",
            },
            {
                "start": "19990201",
                "end": "20000201",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh00,esz99,esu99,esm99,esh99,esz98",
            },
            {
                "start": "20070905",
                "end": "20081205",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh09,esz08,esu08,esm08,esh08,esz07,esu07,esm07",
            },
            {
                "start": "19980101",
                "end": "19990101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh99,esz98,esu98,esm98,esh98",
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "gcj19,gcg19,gcz18,gcv18,gcq18,gcm18,gcj18,gcg18,gcz17,gcv17",
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "gcj98,gcg98,gcz97,gcv97,gcq97,gcm97,gcj97,gcg97",
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "clj19,clh19,clg19,clf19,clz18,clx18,clv18,clu18,clq18,cln18,clm18,clk18,clj18,clh18,clg18,clf18,clz17,clx17",
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "clj98,clh98,clg98,clf98,clz97,clx97,clv97,clu97,clq97,cln97,clm97,clk97,clj97,clh97,clg97,clf97",
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
            read_data=True,
        )
        self.assertListEqual([c.code() for c in cs], expect_list.split(","))


if __name__ == "__main__":
    unittest.main()
