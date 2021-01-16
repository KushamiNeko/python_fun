import json
import os
import re
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd
from matplotlib import axes
from matplotlib import font_manager as fm

from fun.data.source import FREQUENCY, DAILY, WEEKLY
from fun.plotter.plotter import Plotter, TextPlotter
from fun.utils import colors, pretty


class StudyZone(Plotter):
    def __init__(
        self,
        symbol: str,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        candlesticks_body_width: float = 0.6,
        # color_long_entry: str = colors.PAPER_PURPLE_900,
        # color_short_entry: str = colors.PAPER_INDIGO_900,
        color_entry: str = colors.PAPER_BROWN_700,
        color_close: str = colors.PAPER_GREEN_700,
        color_warning: str = colors.PAPER_LIME_900,
        alpha: float = 0.3,
    ) -> None:
        assert quotes is not None

        root = os.path.join(
            os.getenv("HOME"), "Documents", "TRADING_NOTES", "study_zone"
        )
        # path = os.path.join(root, f"{symbol.lower()}.json")

        self._symbol = symbol
        self._quotes = quotes
        self._frequency = frequency

        self._candlesticks_body_width = candlesticks_body_width

        # self._color_long_entry = color_long_entry
        # self._color_short_entry = color_short_entry
        self._color_entry = color_entry
        self._color_close = color_close
        self._color_warning = color_warning

        self._alpha = alpha

        self._studies = None

        for r in os.listdir(root):
            pattern = r"[&_,|]"
            targets = re.split(pattern, r)
            targets = list(map(lambda x: x.strip(), targets))

            if self._symbol.lower() in targets:
                path = os.path.join(root, r)
                assert os.path.exists(path)
                for f in os.listdir(path):
                    with open(os.path.join(path, f), "r") as src:
                        try:
                            if self._studies is None:
                                self._studies = json.load(src)
                            else:
                                self._studies.extend(json.load(src))
                        except json.JSONDecodeError:
                            pretty.color_print(
                                colors.PAPER_RED_400,
                                f"invalid json file for trading study zone: {path}",
                            )
                            self._studies = None

                break

    def plot(self, ax: axes.Axes) -> None:
        if self._studies is None:
            return

        if self._frequency != DAILY and self._frequency != WEEKLY:
            return

        mn, mx = ax.get_ylim()

        for study in self._studies:
            start = datetime.strptime(study["start"], "%Y%m%d")
            end = datetime.strptime(study["end"], "%Y%m%d")

            if self._frequency == WEEKLY:
                start = start - timedelta(days=start.weekday())
                end = end - timedelta(days=end.weekday())

            try:

                start_index = self._quotes.index.get_loc(
                    start,
                    # method="nearest",
                )

                end_index = self._quotes.index.get_loc(
                    end,
                    # method="nearest",
                )

            except KeyError:
                continue

            color = ""
            if study["operation"] == "long":
                # color = self._color_long_entry
                color = self._color_entry
            elif study["operation"] == "short":
                # color = self._color_short_entry
                color = self._color_entry
            elif study["operation"] == "close":
                color = self._color_close
            elif study["operation"] == "warning":
                color = self._color_warning
            else:
                raise ValueError(f"invalid study operation: {study['operation']}")

            ax.bar(
                start_index - (self._candlesticks_body_width / 2.0),
                width=(end_index - start_index) + self._candlesticks_body_width,
                bottom=mn,
                height=mx - mn,
                align="edge",
                color=color,
                alpha=self._alpha,
            )


class Notes(Plotter):
    def __init__(
        self,
        symbol: str,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        color_long: str = colors.PAPER_PURPLE_400,
        color_short: str = colors.PAPER_INDIGO_400,
        color_close: str = colors.PAPER_GREEN_400,
        alpha: float = 0.85,
        line_width: float = 1.75,
    ) -> None:
        assert quotes is not None

        root = os.path.join(
            os.getenv("HOME"), "Documents", "TRADING_NOTES", "note_anchors"
        )
        path = os.path.join(root, f"{symbol.lower()}.json")

        self._symbol = symbol
        self._quotes = quotes
        self._frequency = frequency

        self._anchors = None
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    self._anchors = json.load(f)
                except json.JSONDecodeError:
                    pretty.color_print(
                        colors.PAPER_RED_400,
                        f"invalid json file for trading note anchors: {path}",
                    )
                    self._anchors = None

        self._color_long = color_long
        self._color_short = color_short
        self._color_close = color_close
        self._alpha = alpha

        self._line_width = line_width

    def _y_offset_ratio(self) -> float:
        offset_ratio = 0.0005

        mn = np.amin(self._quotes.loc[:, "low"])
        mx = np.amax(self._quotes.loc[:, "high"])

        mid = (mn + mx) / 2.0

        ratio = (mx - mid) / mid

        if ratio < 0.1:
            offset_ratio = 0.0007
        elif ratio < 0.5:
            offset_ratio = 0.002
        else:
            offset_ratio = 0.01

        return offset_ratio

    def _read_note(self, date: str) -> Optional[str]:
        root = os.path.join(
            os.getenv("HOME"),
            "Documents",
            "TRADING_NOTES",
            "notes",
            self._symbol.lower(),
        )

        file_regex = re.compile(r"(\d{8})(?:-(\d{8}))*([$#]*).txt")

        try:
            for f in os.listdir(root):
                m = file_regex.match(f)
                assert m is not None

                start = m.group(1)
                end = m.group(2)

                assert start is not None

                if date == start or (end is not None and date == end):
                    with open(os.path.join(root, f), "r") as note_file:
                        note = note_file.read()

                        note_regex = re.compile(
                            r"^[&]*\s*\w+:\s*(\d{8})", flags=re.MULTILINE
                        )

                        ns = note_regex.split(note)

                        for i, n in enumerate(ns):
                            n = n.strip()
                            if n == "":
                                continue
                            else:
                                if n == date:
                                    return ns[i + 1].strip()

        except FileNotFoundError:
            pretty.color_print(
                colors.PAPER_RED_400,
                f"no trading notes file for {self._symbol}",
            )

        return None

    def plot(self, ax: axes.Axes) -> None:
        if self._anchors is None:
            return

        if self._frequency != DAILY and self._frequency != WEEKLY:
            return

        for anchor in self._anchors:
            note = self._read_note(anchor["date"])
            if note is None:
                continue

            date = datetime.strptime(anchor["date"], "%Y%m%d")
            anchorX_date = datetime.strptime(anchor["noteAnchorX"], "%Y%m%d")

            if self._frequency == WEEKLY:
                date = date - timedelta(days=date.weekday())
                anchorX_date = anchorX_date - timedelta(days=anchorX_date.weekday())

            try:

                anchorX = self._quotes.index.get_loc(
                    anchorX_date,
                    # method="nearest",
                )

                x = self._quotes.index.get_loc(
                    date,
                    # method="nearest",
                )

            except KeyError:
                continue

            anchorY = float(anchor["noteAnchorY"])

            y = None
            if anchorY >= self._quotes.iloc[x]["high"]:
                y = self._quotes.iloc[x]["high"] * (1 + self._y_offset_ratio())
            elif anchorY <= self._quotes.iloc[x]["low"]:
                y = self._quotes.iloc[x]["high"] * (1 - self._y_offset_ratio())
            else:
                raise ValueError(
                    f"invalid note anchor for {self._symbol} at {anchor['date']}"
                )

            assert y is not None

            ax.plot(
                [x, anchorX],
                [y, anchorY],
                color=self._color_long,
                alpha=self._alpha,
                linewidth=self._line_width,
            )

            ax.text(
                anchorX,
                anchorY,
                note,
                color="w",
                fontproperties=fm.FontProperties(size=5.0),
                # ha=anchor["horizontal"],
                va=anchor["vertical"],
                wrap=True,
            )


class NoteMarker(TextPlotter):
    def __init__(
        self,
        symbol: str,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        font_color: str = "w",
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

        self._symbol = symbol

        self._quotes = quotes
        self._frequency = frequency

        root = os.path.join(
            os.getenv("HOME"),
            "Documents",
            "TRADING_NOTES",
            "notes",
        )

        self._notes_root = None
        for r in os.listdir(root):
            pattern = r"[&_,|]"

            targets = re.split(pattern, r)
            targets = list(map(lambda x: x.strip(), targets))

            if self._symbol.lower() in targets:
                path = os.path.join(root, r)
                if os.path.exists(path):
                    self._notes_root = path
                break

    def _plot_text(self, ax, highs, lows, middle, offset, x, text):
        high = highs.iloc[x]
        low = lows.iloc[x]
        m = (high + low) / 2.0

        va = "bottom" if m > middle else "top"
        y = low - offset if va == "top" else high + offset

        ax.text(
            x,
            y,
            text,
            color=self._font_color,
            fontproperties=self._font_properties,
            ha="center",
            va=va,
        )

    def _append_note(self, notes, dtime, text):
        try:
            x = self._quotes.index.get_loc(
                dtime,
            )

        except KeyError:
            return

        if x not in notes:
            notes[x] = [text]
        else:
            if text not in notes[x]:
                notes[x].append(text)

    def plot(self, ax: axes.Axes) -> None:
        if self._notes_root is None:
            return

        if len(self._quotes) == 0:
            return

        if self._frequency != DAILY and self._frequency != WEEKLY:
            return

        assert ax is not None

        file_regex = re.compile(r"(\d{8})(?:-(\d{8}))*([$#]*).txt")

        notes = {}

        for f in os.listdir(self._notes_root):
            m = file_regex.match(f)
            assert m is not None

            start = m.group(1)
            end = m.group(2)
            pattern = m.group(3)

            text = "&"
            if pattern is not None:
                if "$" in pattern:
                    text = "$"
                elif "#" in pattern:
                    text = "#"

            assert start is not None

            start_datetime = datetime.strptime(start, "%Y%m%d")

            if self._frequency == WEEKLY:
                start_datetime = start_datetime - timedelta(
                    days=start_datetime.weekday()
                )

            self._append_note(notes, start_datetime, text)

            if end is not None:
                end_datetime = datetime.strptime(end, "%Y%m%d")

                if self._frequency == WEEKLY:
                    end_datetime = end_datetime - timedelta(days=end_datetime.weekday())

                self._append_note(notes, end_datetime, text)

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]

        mx = highs.max()
        mn = lows.min()
        mr = mx - mn

        middle = (mx + mn) / 2.0
        offset = mr * 0.0075

        for x, text in notes.items():
            self._plot_text(
                ax,
                highs,
                lows,
                middle,
                offset,
                x,
                "\n".join(text),
            )
