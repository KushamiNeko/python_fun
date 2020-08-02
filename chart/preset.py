import io
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, cast

import pandas as pd
from fun.chart.base import CHART_SIZE, MEDIUM_CHART
from fun.chart.cache import QuotesCache
from fun.chart.setting import Setting
from fun.chart.static import TradingChart
from fun.chart.theme import MagicalTheme, Theme
from fun.data.source import (
    DAILY,
    DataSource,
    FREQUENCY,
    HOURLY,
    InvestingCom,
    MONTHLY,
    StockCharts,
    WEEKLY,
    Yahoo,
)
from fun.futures.continuous import ContinuousContract
from fun.plotter.background import BackgroundTimeRangeMark
from fun.plotter.candlesticks import CandleSticks
from fun.plotter.entry import EntryZone
from fun.plotter.ibd import DistributionsDay
from fun.plotter.indicator import BollingerBand, SimpleMovingAverage
from fun.plotter.plotter import Plotter
from fun.plotter.quote import LastQuote
from fun.plotter.volatility import VolatilityLevel, VolatilitySummary
from fun.plotter.zone import VolatilityZone


class CandleSticksPreset:
    def __init__(
            self,
            dtime: datetime,
            symbol: str,
            frequency: FREQUENCY,
            # theme: Optional[Theme] = None,
            # theme: Theme = Theme(),
            # setting: Setting=Setting(),
            chart_size: CHART_SIZE = MEDIUM_CHART,
    ) -> None:
        assert re.match(r"^[a-zA-Z0-9]+$", symbol) is not None

        self._symbol = symbol

        assert frequency in (DAILY, WEEKLY, MONTHLY)

        self._frequency = frequency

        self._stime, self._etime = self._time_range(dtime)
        self._exstime, self._exetime = self._extime_range()

        self._frequency = frequency

        self._chart_size = chart_size
        self._cache = self._read_chart_data()

        # if theme is None:
        #     self._theme = Theme()
        # else:
        #     self._theme = theme
        # self._theme = theme
        # self._setting = Setting(chart_size=chart_size)
        self._theme = None
        self._setting = None

        self._controller = None
        self._chart = None
        # self._chart = TradingChart(
        #     quotes=self._cache.quotes(), theme=self._theme, chart_size=self._chart_size,
        # )
        # self._last_quote = True
        # self._records: Optional[List[FuturesTransaction]] = None
        # self._params: Dict[str, str] = {}

    def _time_range(self, dtime: datetime) -> Tuple[datetime, datetime]:

        etime = dtime

        stime: datetime
        if self._frequency == HOURLY:
            stime = etime - timedelta(days=15)
        elif self._frequency == DAILY:
            stime = etime - timedelta(days=365)
        elif self._frequency == WEEKLY:
            stime = etime - timedelta(days=365 * 4)
        elif self._frequency == MONTHLY:
            stime = etime - timedelta(days=365 * 18)
        else:
            raise ValueError(f"invalid frequency")

        return stime, etime

    def _extime_range(self) -> Tuple[datetime, datetime]:
        exetime = self._etime + timedelta(days=500)
        exstime = self._stime - timedelta(days=500)

        now = datetime.now()
        if exetime > now:
            exetime = now

        return exstime, exetime

    def _read_chart_data(self) -> QuotesCache:
        print("network")

        src: Optional[DataSource] = None
        # factory = lambda quotes: CandleSticks(
        #     quotes=quotes, chart_size=self._chart_size
        # )

        if self._symbol in ("vix", "vxn", "sml", "ovx", "gvz"):
            src = Yahoo()

        elif self._symbol in ("vstx", "jniv", "vhsi", "vxfxi"):
            src = InvestingCom()

        elif self._symbol in ("vle", "rvx", "tyvix"):
            src = StockCharts()

        elif self._symbol in (
                "spx",
                "ndx",
                "compq",
                "nya",
                "nikk",
                "ezu",
                "eem",
                "hsi",
                "fxi",
        ):
            src = Yahoo()

        elif self._symbol in (
                "gsy",
                "near",
                "icsh",
                "shv",
                "hyg",
                "ushy",
                "shyg",
                "emb",
                "lqd",
                "igsb",
                "igib",
                "shy",
                "iei",
                "ief",
                "govt",
                "iyr",
                "reet",
                "rem",
        ):
            # src = AlphaVantage()
            src = Yahoo()

        df: pd.DataFrame
        if src is None:
            df = ContinuousContract().read(
                    start=self._exstime,
                    end=self._exetime,
                    symbol=self._symbol,
                    frequency=self._frequency,
            )
        else:
            df = src.read(
                    start=self._exstime,
                    end=self._exetime,
                    symbol=self._symbol,
                    frequency=self._frequency,
            )

        assert df is not None

        # cache = QuotesCache(df, self._stime, self._etime, chart_factory=factory)
        cache = QuotesCache(df, self._stime, self._etime)
        return cache

    # @abstractmethod
    # def make_plotters(
    #     self,
    #     parameters: Optional[List[str]] = None,
    #     additional_plotters: Optional[List[Plotter]] = None,
    # ) -> List[Plotter]:
    # ps = [
    #     SimpleMovingAverage(
    #         n=5,
    #         quotes=self._cache.full_quotes(),
    #         slice_start=self._cache.quotes().index[0],
    #         slice_end=self._cache.quotes().index[-1],
    #         line_color=self._theme.get_color("sma0"),
    #         line_alpha=self._theme.get_alpha("sma"),
    #         line_width=self._setting.linewidth(),
    #     ),
    #     SimpleMovingAverage(
    #         n=20,
    #         quotes=self._cache.full_quotes(),
    #         slice_start=self._cache.quotes().index[0],
    #         slice_end=self._cache.quotes().index[-1],
    #         line_color=self._theme.get_color("sma1"),
    #         line_alpha=self._theme.get_alpha("sma"),
    #         line_width=self._setting.linewidth(),
    #     ),
    #     BollinggerBand(
    #         n=20,
    #         m=1.5,
    #         quotes=self._cache.full_quotes(),
    #         slice_start=self._cache.quotes().index[0],
    #         slice_end=self._cache.quotes().index[-1],
    #         line_color=self._theme.get_color("bb0"),
    #         line_alpha=self._theme.get_alpha("bb"),
    #         line_width=self._setting.linewidth(),
    #     ),
    #     BollinggerBand(
    #         n=20,
    #         m=2.0,
    #         quotes=self._cache.full_quotes(),
    #         slice_start=self._cache.quotes().index[0],
    #         slice_end=self._cache.quotes().index[-1],
    #         line_color=self._theme.get_color("bb1"),
    #         line_alpha=self._theme.get_alpha("bb"),
    #         line_width=self._setting.linewidth(),
    #     ),
    #     BollinggerBand(
    #         n=20,
    #         m=2.5,
    #         quotes=self._cache.full_quotes(),
    #         slice_start=self._cache.quotes().index[0],
    #         slice_end=self._cache.quotes().index[-1],
    #         line_color=self._theme.get_color("bb2"),
    #         line_alpha=self._theme.get_alpha("bb"),
    #         line_width=self._setting.linewidth(),
    #     ),
    #     BollinggerBand(
    #         n=20,
    #         m=3.0,
    #         quotes=self._cache.full_quotes(),
    #         slice_start=self._cache.quotes().index[0],
    #         slice_end=self._cache.quotes().index[-1],
    #         line_color=self._theme.get_color("bb3"),
    #         line_alpha=self._theme.get_alpha("bb"),
    #         line_width=self._setting.linewidth(),
    #     ),
    #     # LastQuote(
    #     #     quotes=self._cache.quotes(),
    #     #     font_color=self._theme.get_color("text"),
    #     #     font_properties=self._theme.get_font(
    #     #         self._setting.text_fontsize(multiplier=1.5)
    #     #     ),
    #     # ),
    # ]

    # if self._last_quote is True:
    #     ps.append(
    #         LastQuote(
    #             quotes=self._cache.quotes(),
    #             font_color=self._theme.get_color("text"),
    #             font_properties=self._theme.get_font(
    #                 self._setting.text_fontsize(multiplier=1.5)
    #             ),
    #         ),
    #     )

    # if self._records is not None:
    #     ps.append(
    #         LeverageRecords(
    #             quotes=self._cache.quotes(),
    #             frequency=self._frequency,
    #             records=self._records,
    #             font_color=self._theme.get_color("text"),
    #             font_properties=self._theme.get_font(self._setting.text_fontsize()),
    #         )
    #     )

    # if self._params is not None and len(self._params) != 0:
    #     if self._symbol in ("vix", "vxn", "rvx", "vstx", "jniv"):
    #         dtime = self._params.get("vixzone", None)
    #         op = self._params.get("vixop", None)
    #         if dtime is not None and op is not None:
    #             ps.append(
    #                 VolatilityZone(
    #                     quotes=self._cache.quotes(),
    #                     dtime=datetime.strptime(dtime, "%Y%m%d"),
    #                     op=op,
    #                 )
    #             )

    # ps = []
    #
    # if plotters is not None:
    #     ps.extend(plotters)
    #
    # return ps
    # raise NotImplementedError

    # def set_parameters(self, params: Dict[str, str]) -> None:
    #     self._params = params
    #
    # def show_records(self, records: Optional[List[FuturesTransaction]] = None) -> None:
    #     if records is not None and len(records) > 0:
    #         self._records = records
    #     else:
    #         self._records = None

    # def show_last_quote(self, show: bool) -> None:
    #     self._last_quote = show

    def cache(self) -> QuotesCache:
        return self._cache

    def full_quotes(self) -> pd.DataFrame:
        return self._cache.full_quotes()

    def quotes(self) -> pd.DataFrame:
        return self._cache.quotes()

    def theme(self) -> Optional[Theme]:
        return self._theme

    def setting(self) -> Optional[Setting]:
        return self._setting

    # def set_theme(self, theme: Theme) -> None:
    #     self._theme = theme
    #     # self._cache.new_theme(theme)
    #
    # def set_setting(self, setting: Setting) -> None:
    #     self._setting = setting

    def last_quote(self) -> Dict[str, Any]:
        df = self._cache.quotes().iloc[-1]
        return {
            "date":     self._cache.quotes().index[-1].strftime("%Y%m%d"),
            "open":     df.get("open"),
            "high":     df.get("high"),
            "low":      df.get("low"),
            "close":    df.get("close"),
            "volume":   df.get("volume", 0),
            "interest": df.get("open interest", 0),
        }

    def time_slice(self, dtime: datetime) -> None:
        stime, etime = self._time_range(dtime)

        if (
                stime <= self._exstime
                or stime >= self._exetime
                or etime <= self._exstime
                or etime >= self._exetime
        ):
            self._stime = stime
            self._etime = etime
            self._exstime, self._exetime = self._extime_range()
            self._cache = self._read_chart_data()
        else:
            self._cache.time_slice(stime, etime)

    def stime(self) -> datetime:
        return cast(datetime, self._cache.stime().to_pydatetime())

    def etime(self) -> datetime:
        return cast(datetime, self._cache.etime().to_pydatetime())

    def exstime(self) -> datetime:
        return cast(datetime, self._cache.exstime().to_pydatetime())

    def exetime(self) -> datetime:
        return cast(datetime, self._cache.exetime().to_pydatetime())

    def forward(self) -> bool:
        # chart = self._cache.forward()
        # if chart is None:
        #     return False
        # else:
        #     return True
        return self._cache.forward()

    def backward(self) -> bool:
        # chart = self._cache.backward()
        # if chart is None:
        #     return False
        # else:
        #     return True
        return self._cache.backward()

    def make_controller(
            self,
            parameters: Optional[Dict[str, str]],
            preset_key: str = "Preset",
            # setting_key: str = "s",
    ) -> None:
        if parameters is None:
            return

        preset = parameters.get(preset_key, "").strip()
        # setting = parameters.get(setting_key, "").strip().split(",")
        if preset == "KushamiNeko":
            self._controller = KushamiNekoController(
                    cache=self._cache,
                    symbol=self._symbol,
                    frequency=self._frequency,
                    # setting=self._setting,
                    chart_size=self._chart_size,
                    parameters=parameters,
            )
        elif preset == "Magical":
            self._controller = MagicalController(
                    cache=self._cache,
                    symbol=self._symbol,
                    frequency=self._frequency,
                    # setting=self._setting,
                    chart_size=self._chart_size,
                    parameters=parameters,
            )

    # def render(self, plotters: Optional[List[Plotter]] = None) -> io.BytesIO:
    # def render(self, controller: Optional[PresetController] = None,
    def render(self, additional_plotters: Optional[List[Plotter]] = None) -> io.BytesIO:

        buf = io.BytesIO()

        # self._cache.chart().render(buf, plotters=self._make_plotters(plotters=plotters))

        plotters = []
        # if controller is not None:
        #     # controller.set_cache(self._cache)
        #     # controller.set_frequency(self._frequency)
        #     # controller.set_setting(self._setting)
        #
        #     self._theme = controller.get_theme()
        #     plotters = controller.get_plotters()

        if self._controller is not None:
            self._theme = self._controller.get_theme()
            self._setting = self._controller.get_setting()
            plotters.extend(self._controller.get_plotters())

        if additional_plotters is not None and len(additional_plotters) > 0:
            plotters.extend(additional_plotters)

        self._chart = TradingChart(
                # quotes=self._cache.quotes(), theme=self._theme, chart_size=self._chart_size,
                quotes=self._cache.quotes(),
                theme=self._theme,
                setting=self._setting,
        )

        self._chart.render(buf, plotters=plotters)

        buf.seek(0)

        return buf

    def inspect(
            self,
            x: float,
            y: float,
            ax: Optional[float] = None,
            ay: Optional[float] = None,
            decimals: int = 2,
    ) -> Optional[Dict[str, str]]:
        # n = self._cache.chart().to_data_coordinates(x, y)
        n = self._chart.to_data_coordinates(x, y)
        if n is None:
            return None

        nx, ny = n

        df = self._cache.quotes()

        info = {
            "date":     self._cache.quotes().index[nx].strftime("%Y-%m-%d"),
            "price":    f"{ny:,.{decimals}f}",
            "open":     f"{df.iloc[nx].get('open'):,.{decimals}f}",
            "high":     f"{df.iloc[nx].get('high'):,.{decimals}f}",
            "low":      f"{df.iloc[nx].get('low'):,.{decimals}f}",
            "close":    f"{df.iloc[nx].get('close'):,.{decimals}f}",
            "volume":   f"{df.iloc[nx].get('volume', 0):,.0f}",
            "interest": f"{df.iloc[nx].get('open interest', 0):,.0f}",
        }

        if ax is None or ay is None:
            if nx != 0:
                base = self._cache.quotes().iloc[nx - 1].get("close")
                info["diff($)"] = f"{df.iloc[nx].get('close') - base:,.{decimals}f}"

                info[
                    "diff(%)"
                ] = f"{((df.iloc[nx].get('close') - base) / base) * 100.0:,.{decimals}f}"

        else:
            # an = self._cache.chart().to_data_coordinates(ax, ay)
            an = self._chart.to_data_coordinates(ax, ay)
            assert an is not None

            ax, ay = an

            base_date = self._cache.quotes().index[ax]

            info["diff(d)"] = f"{(df.index[nx] - base_date).days}"
            info["diff(w)"] = f"{(df.index[nx] - base_date).days // 7}"
            info["diff($)"] = f"{ny - ay:,.{decimals}f}"
            info["diff(%)"] = f"{((ny - ay) / ay) * 100.0:,.{decimals}f}"

        return info


class PresetController(metaclass=ABCMeta):

    # def __init__(self, cache: QuotesCache, frequency: FREQUENCY, parameters: Optional[Dict[str, str]]) -> None:
    # def __init__(self, cache: QuotesCache, frequency: FREQUENCY, setting: Setting, parameters: Optional[Dict[str, str]]) -> None:
    def __init__(
            self,
            cache: QuotesCache,
            symbol: str,
            frequency: FREQUENCY,
            # setting: Setting,
            chart_size: CHART_SIZE,
            # parameters: Optional[List[str]],
            parameters: Optional[Dict[str, str]],
    ) -> None:
        self._cache = cache
        self._symbol = symbol
        self._frequency = frequency
        # self._setting = setting

        self._chart_size = chart_size
        self._setting = Setting(chart_size=chart_size)

        self._parameters = parameters

    # def set_cache(self, cache: QuotesCache) -> None:
    #     self._cache = cache
    #
    # def set_frequency(self, frequency: FREQUENCY) -> None:
    #     self._frequency = frequency
    #
    # def set_setting(self, setting: Setting) -> None:
    #     self._setting = setting
    #
    # def set_chart_size(self, chart_size: CHART_SIZE) -> None:
    #     self._setting = Setting(chart_size=chart_size)

    def get_setting(self) -> Setting:
        return self._setting

    @abstractmethod
    def get_theme(self) -> Theme:
        raise NotImplementedError

    @abstractmethod
    # def get_plotters(self, parameters: Optional[Dict[str, str]]) -> List[Plotter]:
    def get_plotters(self) -> List[Plotter]:
        raise NotImplementedError


class KushamiNekoController(PresetController):
    def get_theme(self) -> Theme:
        return Theme()

    def get_plotters(
            self,
            # parameters: Optional[List[str]] = None,
            # additional_plotters: Optional[List[Plotter]] = None,
    ) -> List[Plotter]:
        plotters = [
            BackgroundTimeRangeMark(
                    quotes=self._cache.quotes(), frequency=self._frequency,
            ),
            CandleSticks(
                    quotes=self._cache.quotes(),
                    shadow_width=self._setting.shadow_width(),
                    body_width=self._setting.body_width(),
                    # minimum_height=self._minimum_height(),
                    color_up=self.get_theme().get_color("up"),
                    color_down=self.get_theme().get_color("down"),
                    color_unchanged=self.get_theme().get_color("unchanged"),
            ),
            LastQuote(
                    quotes=self._cache.quotes(),
                    font_color=self.get_theme().get_color("text"),
                    font_properties=self.get_theme().get_font(
                            self._setting.text_fontsize(multiplier=1.5)
                    ),
            ),
            VolatilityLevel(
                    quotes=self._cache.quotes(),
                    symbol=self._symbol,
                    frequency=self._frequency,
                    font_properties=self.get_theme().get_font(
                            self._setting.text_fontsize(multiplier=1.5)
                    ),
            )
        ]

        # theme_set = self._params.get("themeSet", "").strip()
        # theme_setting = self._params.get("themeSetting", "").strip()
        if self._parameters is not None:

            # for setting in self._parameters:
            # if setting == "MovingAverages":
            if self._parameters.get("MovingAverages", "").lower() == "true":
                plotters.extend(
                        [
                            SimpleMovingAverage(
                                    n=5,
                                    quotes=self._cache.full_quotes(),
                                    slice_start=self._cache.quotes().index[0],
                                    slice_end=self._cache.quotes().index[-1],
                                    line_color=self.get_theme().get_color("sma0"),
                                    line_alpha=self.get_theme().get_alpha("sma"),
                                    line_width=self._setting.linewidth(),
                            ),
                            SimpleMovingAverage(
                                    n=20,
                                    quotes=self._cache.full_quotes(),
                                    slice_start=self._cache.quotes().index[0],
                                    slice_end=self._cache.quotes().index[-1],
                                    line_color=self.get_theme().get_color("sma1"),
                                    line_alpha=self.get_theme().get_alpha("sma"),
                                    line_width=self._setting.linewidth(),
                            ),
                            # SimpleMovingAverage(
                            #     n=100,
                            #     quotes=self._cache.full_quotes(),
                            #     slice_start=self._cache.quotes().index[0],
                            #     slice_end=self._cache.quotes().index[-1],
                            #     line_color=self._theme.get_color("sma2"),
                            #     line_alpha=self._theme.get_alpha("sma"),
                            #     line_width=self._setting.linewidth(),
                            # ),
                        ]
                )
            # elif setting == "BollingerBands":
            if self._parameters.get("BollingerBands", "").lower() == "true":
                plotters.extend(
                        [
                            BollingerBand(
                                    n=20,
                                    m=1.5,
                                    quotes=self._cache.full_quotes(),
                                    slice_start=self._cache.quotes().index[0],
                                    slice_end=self._cache.quotes().index[-1],
                                    line_color=self.get_theme().get_color("bb0"),
                                    line_alpha=self.get_theme().get_alpha("bb"),
                                    line_width=self._setting.linewidth(),
                            ),
                            BollingerBand(
                                    n=20,
                                    m=2.0,
                                    quotes=self._cache.full_quotes(),
                                    slice_start=self._cache.quotes().index[0],
                                    slice_end=self._cache.quotes().index[-1],
                                    line_color=self.get_theme().get_color("bb1"),
                                    line_alpha=self.get_theme().get_alpha("bb"),
                                    line_width=self._setting.linewidth(),
                            ),
                            BollingerBand(
                                    n=20,
                                    m=2.5,
                                    quotes=self._cache.full_quotes(),
                                    slice_start=self._cache.quotes().index[0],
                                    slice_end=self._cache.quotes().index[-1],
                                    line_color=self.get_theme().get_color("bb2"),
                                    line_alpha=self.get_theme().get_alpha("bb"),
                                    line_width=self._setting.linewidth(),
                            ),
                            BollingerBand(
                                    n=20,
                                    m=3.0,
                                    quotes=self._cache.full_quotes(),
                                    slice_start=self._cache.quotes().index[0],
                                    slice_end=self._cache.quotes().index[-1],
                                    line_color=self.get_theme().get_color("bb3"),
                                    line_alpha=self.get_theme().get_alpha("bb"),
                                    line_width=self._setting.linewidth(),
                            ),
                        ]
                )
            if self._parameters.get("VixZone", "").lower() == "true":
                if self._symbol in (
                        "vix",
                        "vxn",
                        "rvx",
                        "jniv",
                        "vstx",
                        "vhsi",
                        "vxfxi",
                ):

                    reference = self._parameters.get("VixReferenceDate", "").strip()
                    op = self._parameters.get("VixOp", "").strip()

                    if reference != "" and op != "":
                        plotters.append(
                                VolatilityZone(
                                        quotes=self._cache.quotes(),
                                        dtime=datetime.strptime(reference, "%Y%m%d"),
                                        op=op,
                                )
                        )

            if self._parameters.get("EntryZone", "").lower() == "true":
                notice = self._parameters.get("EntryNoticeDate", "").strip()
                prepare = self._parameters.get("EntryPrepareDate", "").strip()
                op = self._parameters.get("EntryOp", "").strip()

                notice_date = (
                    datetime.strptime(notice, "%Y%m%d") if notice != "" else None
                )
                prepare_date = (
                    datetime.strptime(prepare, "%Y%m%d") if prepare != "" else None
                )

                if op != "":
                    plotters.append(
                            EntryZone(
                                    quotes=self._cache.quotes(),
                                    frequency=self._frequency,
                                    operation=op,
                                    notice_signal=notice_date,
                                    prepare_signal=prepare_date,
                            ),
                    )

            if self._parameters.get("DistributionDays", "").lower() == "true":
                plotters.append(
                        DistributionsDay(
                                quotes=self._cache.quotes(),
                                frequency=self._frequency,
                                font_color=self.get_theme().get_color("text"),
                                font_properties=self.get_theme().get_font(
                                        self._setting.text_fontsize()
                                ),
                                info_font_properties=self.get_theme().get_font(
                                        self._setting.text_fontsize(multiplier=1.5)
                                ),
                        )
                )

            if self._parameters.get("VolatilitySummary", "").lower() == "true":
                plotters.append(
                        VolatilitySummary(
                                quotes=self._cache.quotes(),
                                frequency=self._frequency,
                                symbol=self._symbol,
                        )
                )

        return plotters


class MagicalController(PresetController):
    def get_theme(self) -> Theme:
        return MagicalTheme()

    def get_plotters(self) -> List[Plotter]:
        plotters = [
            BackgroundTimeRangeMark(
                    quotes=self._cache.quotes(), frequency=self._frequency,
            ),
            CandleSticks(
                    quotes=self._cache.quotes(),
                    shadow_width=self._setting.shadow_width(),
                    body_width=self._setting.body_width(),
                    # minimum_height=self._minimum_height(),
                    color_up=self.get_theme().get_color("up"),
                    color_down=self.get_theme().get_color("down"),
                    color_unchanged=self.get_theme().get_color("unchanged"),
            ),
            LastQuote(
                    quotes=self._cache.quotes(),
                    font_color=self.get_theme().get_color("text"),
                    font_properties=self.get_theme().get_font(
                            self._setting.text_fontsize(multiplier=1.5)
                    ),
            ),
        ]

        for key, value in self._parameters.items():
            match = re.match(r"^SMA\s*(\d+)$", key)
            if match is not None:
                if value.lower() != "true":
                    continue

                n = int(match.group(1))
                plotters.append(
                        SimpleMovingAverage(
                                n=n,
                                quotes=self._cache.full_quotes(),
                                slice_start=self._cache.quotes().index[0],
                                slice_end=self._cache.quotes().index[-1],
                                line_color=self.get_theme().get_color(f"sma{n}"),
                                line_alpha=self.get_theme().get_alpha("sma"),
                                line_width=self._setting.linewidth(),
                        ),
                )

        # if self._parameters is not None:
        #     numbers = [int(s) for s in self._parameters]
        #     for n in numbers:
        #         plotters.append(
        #             SimpleMovingAverage(
        #                 n=n,
        #                 quotes=self._cache.full_quotes(),
        #                 slice_start=self._cache.quotes().index[0],
        #                 slice_end=self._cache.quotes().index[-1],
        #                 line_color=self.get_theme().get_color(f"sma{n}"),
        #                 line_alpha=self.get_theme().get_alpha("sma"),
        #                 line_width=self._setting.linewidth(),
        #             ),
        #         )

        return plotters

# class BollingerBandsPreset(CandleSticksPreset):
#     def _make_plotters(self, plotters: Optional[List[Plotter]] = None) -> List[Plotter]:
#         ps = [
#             SimpleMovingAverage(
#                 n=5,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("sma0"),
#                 line_alpha=self._theme.get_alpha("sma"),
#                 line_width=self._setting.linewidth(),
#             ),
#             SimpleMovingAverage(
#                 n=20,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("sma1"),
#                 line_alpha=self._theme.get_alpha("sma"),
#                 line_width=self._setting.linewidth(),
#             ),
#             BollingerBand(
#                 n=20,
#                 m=1.5,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("bb0"),
#                 line_alpha=self._theme.get_alpha("bb"),
#                 line_width=self._setting.linewidth(),
#             ),
#             BollingerBand(
#                 n=20,
#                 m=2.0,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("bb1"),
#                 line_alpha=self._theme.get_alpha("bb"),
#                 line_width=self._setting.linewidth(),
#             ),
#             BollingerBand(
#                 n=20,
#                 m=2.5,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("bb2"),
#                 line_alpha=self._theme.get_alpha("bb"),
#                 line_width=self._setting.linewidth(),
#             ),
#             BollingerBand(
#                 n=20,
#                 m=3.0,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("bb3"),
#                 line_alpha=self._theme.get_alpha("bb"),
#                 line_width=self._setting.linewidth(),
#             ),
#         ]
#
#         if plotters is not None:
#             ps.extend(plotters)
#
#         return ps


# class MovingAveragesPreset(CandleSticksPreset):
#     def _make_plotters(self, plotters: Optional[List[Plotter]] = None) -> List[Plotter]:
#         ps = [
#             # SimpleMovingAverage(
#             #     n=3,
#             #     quotes=self._cache.full_quotes(),
#             #     slice_start=self._cache.quotes().index[0],
#             #     slice_end=self._cache.quotes().index[-1],
#             #     line_color=self._theme.get_color("sma2"),
#             #     line_alpha=self._theme.get_alpha("sma"),
#             #     line_width=self._setting.linewidth(),
#             # ),
#             SimpleMovingAverage(
#                 n=5,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("sma0"),
#                 line_alpha=self._theme.get_alpha("sma"),
#                 line_width=self._setting.linewidth(),
#             ),
#             # SimpleMovingAverage(
#             #     n=7,
#             #     quotes=self._cache.full_quotes(),
#             #     slice_start=self._cache.quotes().index[0],
#             #     slice_end=self._cache.quotes().index[-1],
#             #     line_color=self._theme.get_color("sma3"),
#             #     line_alpha=self._theme.get_alpha("sma"),
#             #     line_width=self._setting.linewidth(),
#             # ),
#             # SimpleMovingAverage(
#             #     n=10,
#             #     quotes=self._cache.full_quotes(),
#             #     slice_start=self._cache.quotes().index[0],
#             #     slice_end=self._cache.quotes().index[-1],
#             #     line_color=self._theme.get_color("sma4"),
#             #     line_alpha=self._theme.get_alpha("sma"),
#             #     line_width=self._setting.linewidth(),
#             # ),
#             SimpleMovingAverage(
#                 n=20,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("sma1"),
#                 line_alpha=self._theme.get_alpha("sma"),
#                 line_width=self._setting.linewidth(),
#             ),
#             # SimpleMovingAverage(
#             #     n=30,
#             #     quotes=self._cache.full_quotes(),
#             #     slice_start=self._cache.quotes().index[0],
#             #     slice_end=self._cache.quotes().index[-1],
#             #     line_color=self._theme.get_color("sma5"),
#             #     line_alpha=self._theme.get_alpha("sma"),
#             #     line_width=self._setting.linewidth(),
#             # ),
#             SimpleMovingAverage(
#                 n=50,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("sma2"),
#                 line_alpha=self._theme.get_alpha("sma"),
#                 line_width=self._setting.linewidth(),
#             ),
#             # SimpleMovingAverage(
#             #     n=100,
#             #     quotes=self._cache.full_quotes(),
#             #     slice_start=self._cache.quotes().index[0],
#             #     slice_end=self._cache.quotes().index[-1],
#             #     line_color=self._theme.get_color("sma7"),
#             #     line_alpha=self._theme.get_alpha("sma"),
#             #     line_width=self._setting.linewidth(),
#             # ),
#             SimpleMovingAverage(
#                 n=200,
#                 quotes=self._cache.full_quotes(),
#                 slice_start=self._cache.quotes().index[0],
#                 slice_end=self._cache.quotes().index[-1],
#                 line_color=self._theme.get_color("sma3"),
#                 line_alpha=self._theme.get_alpha("sma"),
#                 line_width=self._setting.linewidth(),
#             ),
#         ]
#
#         if plotters is not None:
#             ps.extend(plotters)
#
#         return ps
