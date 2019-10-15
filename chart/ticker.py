from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from matplotlib import ticker


class Ticker(metaclass=ABCMeta):
    @abstractmethod
    def ticks(self) -> Dict[float, str]:
        raise NotImplementedError


class TimeTicker(Ticker):
    def __init__(self, times: List[datetime]):
        self._times = times

    def ticks(self) -> Dict[float, str]:
        frequency = ""

        start = self._times[0]
        end = self._times[-1]

        period = end - start
        if period.days < 30:
            frequency = "h"
        elif period.days < 365 * 2:
            frequency = "d"
        elif period.days < 365 * 7:
            frequency = "w"
        else:
            frequency = "m"

        loc = []
        last_time = None
        labels: List[str] = []

        for i, t in enumerate(self._times):
            time = t

            if frequency == "d":
                if not last_time:
                    if time.day > 15:
                        continue
                else:
                    if time.month == last_time.month:
                        continue

                last_time = time
                labels.append(time.strftime(r"%Y-%b"))
                loc.append(i)

            elif frequency == "w":
                if not last_time:
                    if time.day > 15:
                        continue
                else:
                    if time.month == last_time.month:
                        continue

                if time.month == 1:
                    labels.append(time.strftime(r"%Y"))
                else:
                    labels.append(time.strftime(r"%b"))

                last_time = time
                loc.append(i)

            elif frequency == "m":
                if time.month == 1:
                    last_time = time
                    labels.append(time.strftime(r"%Y"))
                    loc.append(i)

            elif frequency == "h":
                if not last_time:
                    if time.hour > 12:
                        continue
                else:
                    if time.day == last_time.day:
                        continue

                if not last_time or time.month != last_time.month:
                    labels.append(time.strftime(r"%b"))
                else:
                    labels.append(time.strftime(r"%d"))

                last_time = time
                loc.append(i)

        return {k: v for k, v in zip(loc, labels)}


class StepTicker(Ticker):
    def __init__(
        self,
        mn: float,
        mx: float,
        nbins: int = 25,
        steps: Optional[List[int]] = [1, 2, 5, 10],
    ):
        self._nbins = nbins
        self._steps = steps
        self._min = mn
        self._max = mx

    def ticks(self) -> Dict[float, str]:
        locator = ticker.MaxNLocator(nbins=self._nbins, steps=self._steps)
        values = locator.tick_values(self._min, self._max)

        return {v: f"{v:.2f}" for v in values}
