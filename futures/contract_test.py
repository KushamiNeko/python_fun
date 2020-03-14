import unittest

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    Contract,
)
from fun.utils.testing import parameterized


class TestContract(unittest.TestCase):
    @parameterized(
        [
            {"code": "es", "months": FINANCIAL_CONTRACT_MONTHS, "fmt": "barchart"},
            {"code": "nk225m", "months": FINANCIAL_CONTRACT_MONTHS, "fmt": "quandl"},
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "barchart",
            },
            {"code": "esh20", "months": FINANCIAL_CONTRACT_MONTHS, "fmt": "quandl"},
        ]
    )
    def test_value_error(self, code, months, fmt):
        with self.assertRaises(ValueError):
            Contract(
                code=code, months=months, fmt=fmt, read_data=False,
            )

    @parameterized(
        [
            {"code": "esh20", "months": "hello", "fmt": "barchart"},
            {"code": "esh20", "months": FINANCIAL_CONTRACT_MONTHS, "fmt": "hello"},
        ]
    )
    def test_assert_error(self, code, months, fmt):
        with self.assertRaises(AssertionError):
            Contract(
                code=code, months=months, fmt=fmt, read_data=False,
            )

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
        c = Contract(code=code, months=months, fmt=fmt, read_data=False,)

        self.assertEqual(c.year(), expect_year)
        self.assertEqual(c.month(), expect_month)
        self.assertEqual(c.symbol(), expect_symbol)

        self.assertEqual(
            c.previous_contract(read_data=False).code(), expect_previous_contract_code
        )


if __name__ == "__main__":
    unittest.main()
