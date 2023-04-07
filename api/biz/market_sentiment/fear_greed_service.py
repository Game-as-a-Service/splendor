from typing import List

from api.biz.market_sentiment import MarketSentimentService
from api.common.datetime_utils import date_to_str
from api.common.number_utils import decimal_to_float
from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from dbmodels.nike.market_indicator_current_state import MarketIndicatorCurrentState
from dbmodels.nike.market_indicator_stats import MarketIndicatorStats

INDICATOR = "fear_and_greed_indicator"
FEAR_AND_GREED = {
    5: "極度貪婪",
    4: "極度貪婪",
    3: "貪婪",
    2: "貪婪",
    1: "中立",
    0: "中立",
    -1: "中立",
    -2: "恐懼",
    -3: "恐懼",
    -4: "極度恐懼",
    -5: "極度恐懼"
}


class FearGreedService(MarketSentimentService):

    def current(self) -> dict:
        current_signal: MarketIndicatorCurrentState = self.get_market_indicator_current(INDICATOR)
        data = {
            "text": self._reverse_content(),
            "score": current_signal.value,
            "description": current_signal.description,
            "updatedAt": date_to_str(self.get_data_latest_date(INDICATOR), fmt="%Y/%-m/%-d"),
        }
        return data

    def historical(self) -> dict:
        historical_signals: List[HistoricalMarketIndicator] = self.get_historical_market_indicator(INDICATOR, 5)

        historical = [{
            "score": signal.value,
            "date": date_to_str(signal.date, fmt="%-m/%-d"),
            "text": FEAR_AND_GREED[signal.value]
        } for signal in historical_signals]

        historical.reverse()

        data = {
            "historical": historical,
            "updatedAt": date_to_str(self.get_data_latest_date(INDICATOR), fmt="%Y/%-m/%-d")
        }
        return data

    def reversal_form(self) -> dict:
        form = []
        for status in ["reverse_5", "reverse_4", "reverse_-4", "reverse_-5"]:
            stats: MarketIndicatorStats = self.get_market_indicator_stats(INDICATOR, status)

            form.append({
                "indicatorStatus": stats.indicator_status,
                "avgLoss": decimal_to_float(stats.avg_loss),
                "avgProfit": decimal_to_float(stats.avg_profit),
                "avgProfitAndLoss": decimal_to_float(stats.avg_profit_and_loss),
                "profitability": decimal_to_float(stats.profitability),
                "quantile25": decimal_to_float(stats.quantile_25),
                "quantile50": decimal_to_float(stats.quantile_50),
                "quantile75": decimal_to_float(stats.quantile_75)
            })

        data = {
            "signals": form,
            "text": self._reverse_content(),
            "updatedAt": date_to_str(self.get_data_latest_date(INDICATOR), fmt="%Y/%-m/%-d")
        }
        return data

    def _reverse_content(self) -> str:
        signals: List[HistoricalMarketIndicator] = self.get_historical_market_indicator(INDICATOR, 2)

        now = signals[0].value
        before = signals[1].value

        if before == 5 and now < 5:
            return "reverse_5"
        if before == 4 and now < 4:
            return "reverse_4"
        if before == -5 and now > -5:
            return "reverse_-5"
        if before == -4 and now > -4:
            return "reverse_-4"
        return ""
