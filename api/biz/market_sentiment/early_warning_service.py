from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd

from api.biz.market_sentiment import MarketSentimentService
from api.common.datetime_utils import date_to_str
from api.common.number_utils import decimal_to_float
from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from dbmodels.nike.market_indicator_current_state import MarketIndicatorCurrentState

INDICATOR = "Market_Traffic_Light"
SIGNAL_MAPPING = {
    -1: "warning",
    0: "beware",
    1: "stable"
}
SIGNAL_INDICATOR = {
    "warning": "hist_info_description_-1",
    "beware": "hist_info_description_0",
    "stable": "hist_info_description_1"
}


class EarlyWarningService(MarketSentimentService):

    def current(self) -> dict:
        current_signal: MarketIndicatorCurrentState = self.get_market_indicator_current(INDICATOR)
        data = {
            "signal": SIGNAL_MAPPING[current_signal.value],
            "description": current_signal.description,
            "updatedAt": date_to_str(self.get_data_latest_date(INDICATOR), fmt="%Y/%-m/%-d"),
        }
        return data

    def recent_signals(self) -> dict:
        signals: List[HistoricalMarketIndicator] = self.get_historical_market_indicator(INDICATOR, 5)

        data = {
            "updatedAt": date_to_str(self.get_data_latest_date(INDICATOR), fmt="%Y/%-m/%-d"),
            "oneWeekAgo": SIGNAL_MAPPING[signals[1].value],
            "twoWeekAgo": SIGNAL_MAPPING[signals[2].value],
            "threeWeekAgo": SIGNAL_MAPPING[signals[3].value],
            "fourWeekAgo": SIGNAL_MAPPING[signals[4].value]
        }
        return data

    def historical_signals(self) -> List[dict]:
        price = pd.DataFrame(
            self._symbol_service.get_symbol_price("^GSPC", "2000-01-10", date_to_str(datetime.now()))).drop(
            ["symbol", "time_frame", "open_price", "high_price", "low_price", "close_price", "volume", "adj_open_price",
             "adj_high_price", "adj_low_price", "adj_volume", "return"], axis=1).set_index("time", drop=True)
        signals = pd.DataFrame(self.get_historical_market_indicator_to_dict(INDICATOR)).drop(
            ["id", "indicator", "updated_at", "created_at"], axis=1).set_index("date", drop=True)

        historical = pd.concat([price, signals]).sort_index()
        historical["value"].fillna(method="pad", inplace=True)
        historical.dropna(subset=["adj_close_price"], inplace=True)

        historical["date"] = pd.to_datetime(historical.index).strftime('%Y-%m-%d')
        historical["price"] = historical["adj_close_price"].astype(float)
        historical["signal"] = historical["value"].astype(int)
        historical.drop(["adj_close_price", "value"], axis=1, inplace=True)
        historical.replace(1, "stable", inplace=True)
        historical.replace(0, "beware", inplace=True)
        historical.replace(-1, "warning", inplace=True)

        return historical.to_dict(orient="records")

    def historical_details(
            self,
            signal: str,
            page: int,
            page_size: int,
            sort_by: Optional[str] = None
    ) -> Tuple[dict, int]:
        market_signal_list, total = self.get_market_signal_list(INDICATOR, signal, page, page_size, sort_by)

        content = self.get_market_indicator_current(SIGNAL_INDICATOR[signal]).description

        details = [{
            "startAt": date_to_str(m.start_at),
            "endAt": date_to_str(m.start_at),
            "duration": m.duration,
            "cumReturn": decimal_to_float(m.cum_return),
            "maxDrawdown": decimal_to_float(m.max_drawdown),
            "event": m.event
        } for m in market_signal_list]

        data = {
            "details": details,
            "content": content,
            "updatedAt": date_to_str(self.get_data_latest_date(INDICATOR), fmt="%Y/%-m/%-d")
        }
        return data, total
