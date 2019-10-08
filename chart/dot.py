import math
from typing import Callable, List, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import scipy


class DotPatches:
    def __init__(
        self,
        data: List[List[float]],
        data_round: bool = True,
        data_ndigits: int = 0,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        text: str = "",
        title_font_size: int = 14,
        label_font_size: int = 10,
        tick_font_size: int = 8,
        text_font_size: int = 8,
        group_width: int = 1,
        ymargin: float = 1,
        point_size: float = 0.05,
        point_padding: float = 1.25,
        point_alpha: float = 1,
        point_colors: List[str] = ["#ff0000", "#00ff48", "#0088ff"],
        xticklabels: List[str] = [],
        line_colors: List[str] = ["#000000", "#000000", "#000000"],
        line_alpha: float = 1,
        line_width: float = 2,
        line_length: float = 7,
        line_style: str = "-.",
        legend: bool = False,
        calc: str = "none",
        dpi: int = 500,
        output: str = "out.png",
    ):
        self._data = data

        self._data_round = data_round
        self._data_ndigits = data_ndigits

        self._title = title
        self._xlabel = xlabel
        self._ylabel = ylabel

        self._text = text

        self._title_font_size = title_font_size
        self._label_font_size = label_font_size
        self._tick_font_size = tick_font_size

        self._text_font_size = text_font_size

        self._group_width = group_width

        self._ymargin = ymargin

        self._point_size = point_size
        self._point_padding = point_padding

        self._point_colors = point_colors
        self._point_alpha = point_alpha

        self._line_width = line_width
        self._line_length = line_length / 10.0
        self._line_style = line_style
        self._line_colors = line_colors if line_colors else point_colors
        self._line_alpha = line_alpha

        self._legend = legend

        self._calc = calc

        self._xticklabels = xticklabels
        self._dpi = dpi

        self._output = output

    @classmethod
    def _data_range(
        cls, data: List[List[float]], rounding: bool, ndigits: int
    ) -> Tuple[float, float]:
        if rounding:
            mx = max([x for d in data for x in d])
            mn = min([x for d in data for x in d])
            return (mx, mn)
        else:
            mx = max([round(x, ndigits) for d in data for x in d])
            mn = min([round(x, ndigits) for d in data for x in d])
            return (mx, mn)

    @classmethod
    def _count_value(
        cls, data: List[float], val: float, rounding: bool = True, ndigits: int = 2
    ) -> int:
        num = 0
        for v in data:
            nv = v
            nval = val
            if rounding:
                nv = round(v, ndigits)
                nval = round(val, ndigits)

            if nv == nval:
                num += 1

        return num

    @classmethod
    def _offset(cls, v: float) -> List[float]:
        n = math.floor(v / 2)
        if v % 2 == 0:
            r = []
            for x in range(-n, n + 1):
                if x == 0:
                    continue
                if abs(x) == 1:
                    r.append(0.5 * x)
                else:
                    if x > 0:
                        r.append(x - 1 + 0.5)
                    else:
                        r.append(x + 1 - 0.5)

            return r
        else:
            return [x for x in range(-n, n + 1)]

    def plot(self):
        fig, ax = plt.subplots()

        mx, mn = self._data_range(
            self._data, rounding=self._data_round, ndigits=self._data_ndigits
        )

        ax.set_xlim(0, (len(self._data) + 1) * self._group_width)

        ax.set_ylim(
            mn - self._point_size - self._ymargin, mx + self._point_size + self._ymargin
        )

        xlim = (len(self._data) + 1) * self._group_width

        ylim = (mx + self._point_size + self._ymargin) - (
            mn - self._point_size - self._ymargin
        )

        ls = []

        ps = []

        m = None

        for i, d in enumerate(self._data):
            ni = (i + 1) * self._group_width

            ls.append(ni)

            color = None
            line_color = None
            label = None
            try:
                color = self._point_colors[i]
                line_color = self._line_colors[i]
                label = self._xticklabels[i]
            except IndexError:
                pass

            p = patches.Patch(color=color, label=label)
            ps.append(p)

            for v in d:
                nv = v

                if self._data_round:
                    nv = round(v, self._data_ndigits)

                x = ni

                for of in self._offset(
                    self._count_value(
                        d, v, rounding=self._data_round, ndigits=self._data_ndigits
                    )
                ):

                    nx = x + (self._point_size * (of * self._point_padding))

                    rw = self._point_size
                    rh = rw * (ylim / xlim) * (fig.get_figwidth() / fig.get_figheight())

                    c = patches.Ellipse(
                        (nx, nv), rw, rh, color=color, alpha=self._point_alpha
                    )

                    ax.add_patch(c)

            if self._calc == "mean":
                m = scipy.mean(d)
            elif self._calc == "median":
                m = scipy.median(d)

            if m:
                ax.plot(
                    [ni - self._line_length / 2.0, ni + self._line_length / 2.0],
                    [m, m],
                    self._line_style,
                    color=line_color,
                    linewidth=self._line_width,
                    alpha=self._line_alpha,
                )

        if self._text:
            ax.text(
                1,
                1,
                self._text,
                horizontalalignment="right",
                verticalalignment="top",
                transform=ax.transAxes,
            )

        if self._xticklabels:
            ax.set_xticks(ls)
            ax.set_xticklabels(self._xticklabels, fontsize=self._tick_font_size)

        for label in ax.get_yticklabels():
            label.set_fontsize(self._tick_font_size)

        if self._legend and self._xticklabels:
            ax.legend(handles=ps)

        ax.set_title(self._title, fontsize=self._title_font_size)
        ax.set_xlabel(self._xlabel, fontsize=self._label_font_size)
        ax.set_ylabel(self._ylabel, fontsize=self._label_font_size)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.savefig(self._output, dpi=self._dpi, bbox_inches="tight")
        fig.clear()
        plt.close()


class DotScatter:
    def __init__(
        self,
        data: List[List[float]],
        data_round: bool = True,
        data_ndigits: int = 0,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        text: str = "",
        title_font_size: int = 14,
        label_font_size: int = 10,
        tick_font_size: int = 8,
        text_font_size: int = 8,
        group_width: int = 1,
        ymargin: float = 1,
        point_size: float = 20,
        point_padding: float = 0.07,
        point_alpha: float = 1,
        point_colors: List[str] = ["#ff0000", "#00ff48", "#0088ff"],
        xticklabels: List[str] = [],
        line_colors: List[str] = ["#000000", "#000000", "#000000"],
        line_alpha: float = 1,
        line_width: float = 2,
        line_length: float = 7,
        line_style: str = "-.",
        legend: bool = False,
        calc: str = "none",
        dpi: int = 500,
        output: str = "out.png",
    ):
        self._data = data

        self._data_round = data_round
        self._data_ndigits = data_ndigits

        self._title = title
        self._xlabel = xlabel
        self._ylabel = ylabel

        self._text = text

        self._title_font_size = title_font_size
        self._label_font_size = label_font_size
        self._tick_font_size = tick_font_size

        self._text_font_size = text_font_size

        self._group_width = group_width

        self._ymargin = ymargin

        self._point_size = point_size
        self._point_padding = point_padding
        self._point_colors = point_colors
        self._point_alpha = point_alpha

        self._line_width = line_width
        self._line_length = line_length / 10.0
        self._line_style = line_style
        self._line_colors = line_colors if line_colors else point_colors
        self._line_alpha = line_alpha

        self._legend = legend

        self._calc = calc

        self._xticklabels = xticklabels
        self._dpi = dpi

        self._output = output

    @classmethod
    def _data_max(cls, data: List[List[float]]) -> float:
        return max([x for d in data for x in d])

    @classmethod
    def _data_min(cls, data: List[List[float]]) -> float:
        return min([x for d in data for x in d])

    @classmethod
    def _count_value(
        cls, data: List[float], val: float, preprocess: Callable[[float], float] = None
    ) -> int:
        num = 0
        for v in data:
            nv = v
            nval = val
            if preprocess:
                nv = preprocess(v)
                nval = preprocess(val)

            if nv == nval:
                num += 1

        return num

    @classmethod
    def _offset(cls, v: float) -> List[float]:
        n = math.floor(v / 2)
        if v % 2 == 0:
            r = []
            for x in range(-n, n + 1):
                if x == 0:
                    continue
                if abs(x) == 1:
                    r.append(0.5 * x)
                else:
                    if x > 0:
                        r.append(x - 1 + 0.5)
                    else:
                        r.append(x + 1 - 0.5)

            return r
        else:
            return [x for x in range(-n, n + 1)]

    def plot(self):
        fig, ax = plt.subplots()

        ax.set_xlim(0, (len(self._data) + 1) * self._group_width)

        ax.set_ylim(
            self._data_min(self._data) - self._ymargin,
            self._data_max(self._data) + self._ymargin,
        )

        ls = []

        m = None

        for i, d in enumerate(self._data):
            ni = (i + 1) * self._group_width

            xs = []
            ys = []

            ls.append(ni)

            for v in d:
                nv = v

                if self._data_round:
                    nv = round(v, self._data_ndigits)

                x = ni

                preprocess = None
                if self._data_round:

                    def preprocess(x):
                        return round(x, self._data_ndigits)

                for of in self._offset(self._count_value(d, v, preprocess=preprocess)):

                    nx = x + (self._point_padding * of)

                    xs.append(nx)
                    ys.append(nv)

            color = None
            line_color = None
            label = None
            try:
                color = self._point_colors[i]
                line_color = self._line_colors[i]
                label = self._xticklabels[i]
            except IndexError:
                pass

            ax.scatter(
                xs,
                ys,
                s=self._point_size,
                color=color,
                label=label,
                alpha=self._point_alpha,
            )

            if self._calc == "mean":
                m = scipy.mean(d)
            elif self._calc == "median":
                m = scipy.median(d)

            if m:
                ax.plot(
                    [ni - self._line_length / 2.0, ni + self._line_length / 2.0],
                    [m, m],
                    self._line_style,
                    color=line_color,
                    linewidth=self._line_width,
                    alpha=self._line_alpha,
                )

        if self._text:
            plt.text(
                1,
                1,
                self._text,
                horizontalalignment="right",
                verticalalignment="top",
                transform=ax.transAxes,
            )

        if self._xticklabels:
            plt.xticks(ls, self._xticklabels, fontsize=self._tick_font_size)

        plt.yticks(ax.get_yticks(), fontsize=self._tick_font_size)

        if self._legend and self._xticklabels:
            plt.legend()

        plt.title(self._title, fontsize=self._title_font_size)
        plt.xlabel(self._xlabel, fontsize=self._label_font_size)
        plt.ylabel(self._ylabel, fontsize=self._label_font_size)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.savefig(self._output, dpi=self._dpi, bbox_inches="tight")
        fig.clear()
        plt.close()
