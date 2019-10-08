from __future__ import annotations

import math
from typing import Dict, List

from fun.trading.trade import FuturesTrade


class Statistic:
    # _float_decimals = 4

    def __init__(self, trades: List[FuturesTrade]):

        if not trades:
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
            if trade.pl_dollar > 0:
                self._winners.append(trade)
            elif trade.pl_dollar < 0:
                self._losers.append(trade)

            if trade.operation == "long":
                self._long.append(trade)
            elif trade.operation == "short":
                self._short.append(trade)

            if trade.operation == "long" and trade.pl_dollar > 0:
                self._long_winners.append(trade)
            elif trade.operation == "long" and trade.pl_dollar < 0:
                self._long_losers.append(trade)

            if trade.operation == "short" and trade.pl_dollar > 0:
                self._short_winners.append(trade)
            elif trade.operation == "short" and trade.pl_dollar < 0:
                self._short_losers.append(trade)

    def total_trades(self) -> int:
        return len(self._trades)

    def number_of_winners(self) -> int:
        return len(self._winners)

    def number_of_losers(self) -> int:
        return len(self._losers)

    def batting_average(self) -> float:
        return float(len(self._winners)) / float(self.total_trades())

    def batting_average_long(self) -> float:
        pass

    def winners_pl_mean(self) -> float:
        if len(self._winners) == 0:
            return math.nan

        s = 0.0
        for o in self._winners:
            s += o.pl_dollar

        return s / float(len(self._winners))

    def losers_pl_mean(self) -> float:
        if len(self._losers) == 0:
            return math.nan

        s = 0.0
        for o in self._losers:
            s += o.pl_dollar

        return s / float(len(self._losers))

    def win_loss_ratio(self) -> float:
        return self.winners_pl_mean() / abs(self.losers_pl_mean())

    def adjusted_win_loss_ratio(self) -> float:
        return (self.winners_pl_mean() * self.batting_average()) / (
            abs(self.losers_pl_mean()) * (1.0 - self.batting_average())
        )

    def expected_value(self) -> float:
        return (self.winners_pl_mean() * self.batting_average()) + (
            self.losers_pl_mean() * (1.0 - self.batting_average())
        )

    def kelly_criterion(self) -> float:
        return self.batting_average() - (
            (1.0 - self.batting_average()) / self.win_loss_ratio()
        )

    def to_entity(self) -> Dict[str, str]:
        return {
            "total_trades": str(self.total_trades()),
            "number_of_winners": str(self.number_of_winners()),
            "number_of_losers": str(self.number_of_losers()),
            "batting_average": str(self.batting_average()),
            "win_loss_ratio": str(self.win_loss_ratio()),
            "adjusted_win_loss_ratio": str(self.adjusted_win_loss_ratio()),
            "expected_value": str(self.expected_value()),
            "kelly_criterion": str(self.kelly_criterion()),
        }
