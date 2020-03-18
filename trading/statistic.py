from __future__ import annotations

import math
from typing import Dict, List

from fun.trading.trade import FuturesTrade


class Statistic:
    _float_decimals = 4

    def __init__(self, trades: List[FuturesTrade]) -> None:

        if len(trades) == 0:
            raise ValueError("empty statistic trades")

        self._trades = trades

        self._winners: List[FuturesTrade] = []
        self._losers: List[FuturesTrade] = []

        self._long: List[FuturesTrade] = []
        self._short: List[FuturesTrade] = []

        self._long_winners: List[FuturesTrade] = []
        self._long_losers: List[FuturesTrade] = []

        self._short_winners: List[FuturesTrade] = []
        self._short_losers: List[FuturesTrade] = []

        for trade in self._trades:
            if trade.nominal_profit() > 0:
                self._winners.append(trade)
            elif trade.nominal_profit() < 0:
                self._losers.append(trade)

            if trade.operation() == "+":
                self._long.append(trade)
            elif trade.operation() == "-":
                self._short.append(trade)

            if trade.operation() == "+" and trade.nominal_profit() > 0:
                self._long_winners.append(trade)
            elif trade.operation() == "+" and trade.nominal_profit() < 0:
                self._long_losers.append(trade)

            if trade.operation() == "-" and trade.nominal_profit() > 0:
                self._short_winners.append(trade)
            elif trade.operation() == "-" and trade.nominal_profit() < 0:
                self._short_losers.append(trade)

    def total_trades(self) -> int:
        return len(self._trades)

    def total_long_trades(self) -> int:
        return len(self._long)

    def total_short_trades(self) -> int:
        return len(self._short)

    def number_of_winners(self) -> int:
        return len(self._winners)

    def number_of_long_winners(self) -> int:
        return len(self._long_winners)

    def number_of_short_winners(self) -> int:
        return len(self._short_winners)

    def number_of_losers(self) -> int:
        return len(self._losers)

    def number_of_long_losers(self) -> int:
        return len(self._long_losers)

    def number_of_short_losers(self) -> int:
        return len(self._short_losers)

    def batting_average(self) -> float:
        return float(self.number_of_winners()) / float(self.total_trades())

    def batting_average_long(self) -> float:
        if self.total_long_trades() == 0:
            return math.nan

        return float(self.number_of_long_winners()) / float(self.total_long_trades())

    def batting_average_short(self) -> float:
        if self.total_short_trades() == 0:
            return math.nan

        return float(self.number_of_short_winners()) / float(self.total_short_trades())

    def winners_nominal_profit_mean(self) -> float:
        if self.number_of_winners() == 0:
            return math.nan

        s = 0.0
        for o in self._winners:
            s += o.nominal_profit()

        return s / float(self.number_of_winners())

    def winners_leveraged_profit_mean(self) -> float:
        if self.number_of_winners() == 0:
            return math.nan

        s = 0.0
        for o in self._winners:
            s += o.leveraged_profit()

        return s / float(self.number_of_winners())

    def losers_nominal_profit_mean(self) -> float:
        if self.number_of_losers() == 0:
            return math.nan

        s = 0.0
        for o in self._losers:
            s += o.nominal_profit()

        return s / float(self.number_of_losers())

    def losers_leveraged_profit_mean(self) -> float:
        if self.number_of_losers() == 0:
            return math.nan

        s = 0.0
        for o in self._losers:
            s += o.leveraged_profit()

        return s / float(self.number_of_losers())

    def nominal_win_loss_ratio(self) -> float:
        return self.winners_nominal_profit_mean() / abs(
            self.losers_nominal_profit_mean()
        )

    def leveraged_win_loss_ratio(self) -> float:
        return self.winners_leveraged_profit_mean() / abs(
            self.losers_leveraged_profit_mean()
        )

    def nominal_adjusted_win_loss_ratio(self) -> float:
        return (self.winners_nominal_profit_mean() * self.batting_average()) / (
            abs(self.losers_nominal_profit_mean()) * (1.0 - self.batting_average())
        )

    def leveraged_adjusted_win_loss_ratio(self) -> float:
        return (self.winners_leveraged_profit_mean() * self.batting_average()) / (
            abs(self.losers_leveraged_profit_mean()) * (1.0 - self.batting_average())
        )

    def nominal_expected_value(self) -> float:
        return (self.winners_nominal_profit_mean() * self.batting_average()) + (
            self.losers_nominal_profit_mean() * (1.0 - self.batting_average())
        )

    def leveraged_expected_value(self) -> float:
        return (self.winners_leveraged_profit_mean() * self.batting_average()) + (
            self.losers_leveraged_profit_mean() * (1.0 - self.batting_average())
        )

    def nominal_kelly_criterion(self) -> float:
        return self.batting_average() - (
            (1.0 - self.batting_average()) / self.nominal_win_loss_ratio()
        )

    def to_entity(self) -> Dict[str, str]:
        return {
            "total_trades": f"{self.total_trades()}",
            "number_of_winners": f"{self.number_of_winners()}",
            "number_of_losers": f"{self.number_of_losers()}",
            "batting_average": f"{self.batting_average():.{self._float_decimals}f}%",
            "batting_average_long": f"{self.batting_average_long():.{self._float_decimals}f}%",
            "batting_average_short": f"{self.batting_average_short():.{self._float_decimals}f}%",
            "nominal_win_loss_ratio": f"{self.nominal_win_loss_ratio():.{self._float_decimals}f}",
            "leveraged_win_loss_ratio": f"{self.leveraged_win_loss_ratio():.{self._float_decimals}f}",
            "nominal_adjusted_win_loss_ratio": f"{self.nominal_adjusted_win_loss_ratio():.{self._float_decimals}f}",
            "leveraged_adjusted_win_loss_ratio": f"{self.leveraged_adjusted_win_loss_ratio():.{self._float_decimals}f}",
            "nominal_expected_value": f"{self.nominal_expected_value():.{self._float_decimals}f}%",
            "leveraged_expected_value": f"{self.leveraged_expected_value():.{self._float_decimals}f}%",
        }
