from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from fun.trading.futures_contract_specs import FuturesContractSpecs
from fun.trading.transaction import FuturesTransaction


class FuturesTrade:

    _commission_fees = 1.5

    def __init__(self, orders: List[FuturesTransaction]):

        if not orders:
            raise ValueError("empty trade orders")

        self._orders = sorted(orders, key=lambda o: o.time_stamp)

        self._open_orders: List[FuturesTransaction]
        self._close_orders: List[FuturesTransaction]

        # self._quantity = 0
        # self._average_open = 0.0
        # self._average_close = 0.0
        # self._pl_dollar = 0.0

        self._validate_orders()

    def _validate_orders(self) -> None:
        if (
            self._orders[0].operation not in ("long", "short")
            or self._orders[-1].operation != "close"
        ):
            raise ValueError("invalid trade orders")

        open_orders: List[FuturesTransaction] = []
        close_orders: List[FuturesTransaction] = []

        open_quantity = 0
        close_quantity = 0

        for o in self._orders:
            if o.symbol != self.symbol:
                raise ValueError(
                    f"mismatch symbol in orders: {o.symbol}, {self.symbol}"
                )

            if o.operation in ("long", "short", "increase"):
                open_quantity += o.quantity
                open_orders.append(o)

            elif o.operation in ("decrease", "close"):
                close_quantity += o.quantity
                close_orders.append(o)

        if open_quantity != close_quantity:
            raise ValueError(
                f"quantities of open and close contracts do not match\nopen: {open_quantity}, close: {close_quantity}"
            )

        # self._quantity = open_quantity

        self._open_orders = open_orders
        self._close_orders = close_orders

        # self._average_open = (
        # self._average_price(open_orders)
        # * self._quantity
        # * FuturesContractSpecs.lookup_contract_unit(self.symbol)
        # )

        # if self.operation == "long":
        # self._average_open *= -1

        # self._average_close = (
        # self._average_price(close_orders)
        # * self._quantity
        # * FuturesContractSpecs.lookup_contract_unit(self.symbol)
        # )

        # if self.operation == "short":
        # self._average_close *= -1

        # self._pl_dollar = (
        # self._average_close + self._average_open + self.commission_fees
        # )

    @property
    def operation(self) -> str:
        return self._orders[0].operation

    @property
    def quantity(self) -> int:
        # return self._quantity
        q = 0
        for o in self._open_orders:
            q += o.quantity

        return q

    @property
    def symbol(self) -> str:
        return self._orders[0].symbol

    @property
    def open_time(self) -> datetime:
        return self._orders[0].time

    @property
    def close_time(self) -> datetime:
        return self._orders[-1].time

    @property
    def open_time_stamp(self) -> float:
        return self._orders[0].time_stamp

    @property
    def close_time_stamp(self) -> float:
        return self._orders[-1].time_stamp

    @classmethod
    def _average_price(cls, orders: List[FuturesTransaction]) -> float:
        quantity = 0
        total_price = 0.0

        for order in orders:
            total_price += order.price * order.quantity
            quantity += order.quantity

        return total_price / float(quantity)

    @property
    def average_open(self) -> float:
        # return self._average_open
        average_open = (
            self._average_price(self._open_orders)
            * self.quantity
            * FuturesContractSpecs.lookup_contract_unit(self.symbol)
        )

        if self.operation == "long":
            average_open *= -1

        return average_open

    @property
    def average_close(self) -> float:
        # return self._average_close
        average_close = (
            self._average_price(self._close_orders)
            * self.quantity
            * FuturesContractSpecs.lookup_contract_unit(self.symbol)
        )

        if self.operation == "short":
            average_close *= -1

        return average_close

    @property
    def pl_dollar(self) -> float:
        return self.average_close + self.average_open + self.commission_fees

    @property
    def pl_percent(self) -> float:
        return (self.pl_dollar / abs(self.average_open)) * 100.0

    @property
    def commission_fees(self) -> float:
        return -1 * self._commission_fees * self.quantity * 2

    def to_entity(self) -> Dict[str, str]:
        return {
            "symbol": self.symbol,
            "operation": self.operation,
            "quantity": str(self.quantity),
            "open_time": self.open_time.strftime("%Y-%m-%d"),
            "close_time": self.close_time.strftime("%y-%m-%d"),
            "average_open": str(self.average_open),
            "average_close": str(self.average_close),
            "commission_fees": str(self.commission_fees),
            "pl_dollar": str(self.pl_dollar),
            "pl_percent": f"{self.pl_percent}%",
        }
