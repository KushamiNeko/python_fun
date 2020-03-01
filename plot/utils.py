import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from matplotlib import font_manager as fm


def plot_correlation(
    xs,
    ys,
    ax=None,
    xlabel=None,
    ylabel=None,
    labelsize=14,
    label_len_limit=50,
    pointsize=50,
    linewidth=2,
    font_src=None,
):

    if font_src is not None:
        prop = fm.FontProperties(
            fname=font_src, size=labelsize
        )
    else:
        prop = None

    maxy = ys.max()
    miny = ys.min()

    ry = maxy - miny
    ryratio = 0.2

    tau, p = stats.kendalltau(xs, ys)

    s, i, _, _, _ = stats.linregress(xs.values, ys.values)
    xl = np.linspace(xs.min(), xs.max())

    if ax is None:
        ax = plt.gca()

    ax.set_ylim(
        top=maxy + (ry * ryratio),
        bottom=min(miny, (xs.min() * s) + i) - (ry * (ryratio / 2.0)),
    )

    ax.scatter(xs.values, ys.values, s=pointsize, color="k")
    ax.plot(xl, xl * s + i, color="k", linewidth=linewidth)

    minx, maxx = ax.get_xlim()
    rx = maxx - minx
    rxratio = 0.05

    tx = maxx - (rx * rxratio)
    ha = "right"
    if (
        ys[xs < ((xs.max() + xs.min()) / 2.0)].max()
        < ys[xs > ((xs.max() + xs.min()) / 2.0)].max()
    ):
        tx = minx + (rx * rxratio)
        ha = "left"

    ax.text(
        tx,
        maxy + (ry * (ryratio / 2.0)),
        s=f"P: {round(p, 3):.3f}\nTAU: {round(tau, 3):.3f}",
        color="k",
        ha=ha,
        va="bottom",
        fontproperties=prop,
    )

    if xlabel is not None:
        if len(xlabel) > label_len_limit:
            ax.set_xlabel(
                f"{xlabel[: int(label_len_limit / 2.0)]}.....{xlabel[-int(label_len_limit / 2.0) :]}",
                fontproperties=prop,
            )
        else:
            ax.set_xlabel(xlabel, fontproperties=prop)

    if ylabel is not None:
        if len(ylabel) > label_len_limit:
            ax.set_ylabel(
                f"{ylabel[: int(label_len_limit / 2.0)]}.....{ylabel[-int(label_len_limit / 2.0) :]}",
                fontproperties=prop,
            )
        else:
            ax.set_ylabel(ylabel, fontproperties=prop)
