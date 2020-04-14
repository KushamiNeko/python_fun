from typing import Optional, Tuple

import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.plotter.plotter import TextPlotter


class LastQuote(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        xoffset: float = 3,
        yrange: Optional[Tuple[float, float]] = None,
        font_color: str = "k",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._quotes = quotes

        self._xoffset = xoffset
        if yrange is None:
            self._ymin = np.amin(self._quotes.loc[:, "low"])
            self._ymax = np.amax(self._quotes.loc[:, "high"])
        else:
            self._ymin, self._ymax = yrange

    def plot(self, ax: axes.Axes) -> None:
        if len(self._quotes) > 1:
            quote = self._quotes.iloc[-1]
            prev_quote = self._quotes.iloc[-2]

            text = "\n".join(
                [
                    f"Date:  {self._quotes.index[-1].strftime('%Y-%m-%d')}",
                    f"Open:  {quote.loc['open']:,.2f}",
                    f"High: {quote.loc['high']:,.2f}",
                    f"Low: {quote.loc['low']:,.2f}",
                    f"Close:  {quote.loc['close']:,.2f}",
                    f"Volume:  {int(quote.get('volume', 0)):,}",
                    f"Interest:  {int(quote.get('open interest', 0)):,}",
                    f"Diff($):  {quote.loc['close'] - prev_quote.loc['close']:,.2f}",
                    f"Diff(%):  {((quote.loc['close'] - prev_quote.loc['close'])/prev_quote.loc['close']) * 100.0:,.2f}",
                ]
            )

            h = np.amax(self._quotes.loc[:, "high"])
            l = np.amin(self._quotes.loc[:, "low"])

            lh = np.amax(self._quotes.iloc[:30].loc[:, "high"])
            ll = np.amin(self._quotes.iloc[:30].loc[:, "low"])

            y: float
            va: str
            if abs(l - ll) > abs(h - lh):
                y = np.amin(self._quotes.loc[:, "low"])
                va = "bottom"
            else:
                y = np.amax(self._quotes.loc[:, "high"])
                va = "top"

            ax.text(
                self._xoffset,
                y,
                text,
                color=self._font_color,
                fontproperties=self._font_properties,
                ha="left",
                va=va,
            )
