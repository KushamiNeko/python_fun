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
        chart_height_ratio: float = 0.2,
        # position: str = "auto",
    ):

        # assert position in ("auto", "top", "bottom")

        self._quotes = quotes
        self._body_width = body_width

        self._color_up = color_up
        self._color_down = color_down
        self._color_unchanged = color_unchanged
        self._alpha = alpha

        self._chart_height_ratio = chart_height_ratio
        # self._position = position

    def plot(self, ax: axes.Axes) -> None:
        volumes = self._quotes.get("volume")
        if volumes is None:
            return

        mn, mx = ax.get_ylim()
        max_height = ((mx - mn) * self._chart_height_ratio) + mn

        volumes_max = volumes.max()

        volumes = ((volumes / volumes_max)) * (max_height - mn)
        volumes += mn

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

            body = patches.Rectangle(
                xy=(index - (self._body_width / 2.0), mn),
                width=self._body_width,
                height=volumes.iloc[index] - mn,
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
