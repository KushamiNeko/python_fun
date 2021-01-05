import numpy as np
import pandas as pd
from fun.plotter.plotter import Plotter
from matplotlib import axes, patches
from matplotlib.collections import PatchCollection


class Volume(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        body_width: float,
        color_up: str,
        color_down: str,
        color_unchanged: str,
        alpha: float = 0.35,
        chart_height_ratio: float = 0.15,
        quantile_clamp_ratio: float = 0.95,
    ):

        self._quotes = quotes
        self._body_width = body_width

        self._color_up = color_up
        self._color_down = color_down
        self._color_unchanged = color_unchanged
        self._alpha = alpha

        self._chart_height_ratio = chart_height_ratio
        self._quantile_clamp_ratio = quantile_clamp_ratio

    def plot(self, ax: axes.Axes) -> None:
        volumes = self._quotes.get("volume")
        if volumes is None:
            return

        mn, mx = ax.get_ylim()

        h = np.amax(self._quotes.loc[:, "high"])
        l = np.amin(self._quotes.loc[:, "low"])

        lh = np.amax(self._quotes.iloc[-30:].loc[:, "high"])
        ll = np.amin(self._quotes.iloc[-30:].loc[:, "low"])

        pos_top = False
        if abs(l - ll) > abs(h - lh):
            pos_top = False
        else:
            pos_top = True

        # max_height = ((mx - mn) * self._chart_height_ratio) + mn
        max_height = (mx - mn) * self._chart_height_ratio

        # volumes_max = volumes.max()
        volumes_max = volumes.quantile(self._quantile_clamp_ratio)
        volumes = volumes.clip(upper=volumes_max)

        volumes = ((volumes / volumes_max)) * max_height
        # volumes = ((volumes / volumes_max)) * (max_height - mn)
        # volumes += mn

        length = len(self._quotes)

        bodies = np.ndarray(shape=length, dtype=object)

        for index, df in enumerate(self._quotes.itertuples()):

            p_open = df.open
            p_close = df.close

            color = self._color_unchanged

            if p_close > p_open:
                color = self._color_up
            elif p_close < p_open:
                color = self._color_down

            if not pos_top:
                body = patches.Rectangle(
                    xy=(index - (self._body_width / 2.0), mn),
                    width=self._body_width,
                    # height=volumes.iloc[index] - mn,
                    height=volumes.iloc[index],
                    facecolor=color,
                    edgecolor=color,
                    alpha=self._alpha,
                )

            else:
                body = patches.Rectangle(
                    xy=(index - (self._body_width / 2.0), mx),
                    width=self._body_width,
                    # height=volumes.iloc[index] - mn,
                    height=-volumes.iloc[index],
                    facecolor=color,
                    edgecolor=color,
                    alpha=self._alpha,
                )

            bodies[index] = body

        ax.add_collection(PatchCollection(bodies, match_original=True, zorder=3))

        # ax.plot(
        #     np.arange(len(self._quotes.index)),
        #     volumes.rolling(60).mean(),
        #     color=self._color_unchanged,
        #     alpha=self._alpha,
        #     linewidth=2.5,
        # )

        # interests = self._quotes.get("open interest")

        # if interests is not None:
        #     interests -= interests.min()
        #     interests /= interests.max()

        #     interests *= max_height - mn
        #     interests += mn

        #     ax.plot(
        #         np.arange(len(self._quotes.index)),
        #         interests,
        #         color="r",
        #         alpha=self._alpha,
        #         linewidth=2.5,
        #     )
