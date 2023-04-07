from werkzeug.test import TestResponse

from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from dbmodels.nike.market_indicator_stats import MarketIndicatorStats
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiFearAndGreedReversalSignal(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add_all([
            MarketIndicatorStats(**{
                "indicator": "fear_and_greed_indicator",
                "indicator_status": "reverse_5",
                "profitability": 1.2,
                "avg_profit_and_loss": -0.1,
                "avg_profit": 0.1,
                "avg_loss": 0.2,
                "quantile_25": 0.3,
                "quantile_50": 0.4,
                "quantile_75": 0.5,
            }),
            MarketIndicatorStats(**{
                "indicator": "fear_and_greed_indicator",
                "indicator_status": "reverse_4",
                "profitability": 1.2,
                "avg_profit_and_loss": -0.1,
                "avg_profit": 0.1,
                "avg_loss": 0.2,
                "quantile_25": 0.3,
                "quantile_50": 0.4,
                "quantile_75": 0.5,
            }),
            MarketIndicatorStats(**{
                "indicator": "fear_and_greed_indicator",
                "indicator_status": "reverse_-4",
                "profitability": 1.2,
                "avg_profit_and_loss": -0.1,
                "avg_profit": 0.1,
                "avg_loss": 0.2,
                "quantile_25": 0.3,
                "quantile_50": 0.4,
                "quantile_75": 0.5,
            }),
            MarketIndicatorStats(**{
                "indicator": "fear_and_greed_indicator",
                "indicator_status": "reverse_-5",
                "profitability": 1.2,
                "avg_profit_and_loss": -0.1,
                "avg_profit": 0.1,
                "avg_loss": 0.2,
                "quantile_25": 0.3,
                "quantile_50": 0.4,
                "quantile_75": 0.5,
            }),
        ])
        self.nike_sql_session.add_all([
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "date": "2023-03-14",
                "value": 4
            }),
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "date": "2023-03-13",
                "value": 5
            }),
        ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(MarketIndicatorStats) \
            .filter(MarketIndicatorStats.indicator == "fear_and_greed_indicator") \
            .delete()

        self.nike_sql_session.query(HistoricalMarketIndicator) \
            .filter(HistoricalMarketIndicator.indicator == "fear_and_greed_indicator") \
            .delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/fear-and-greed/reversal-signal123')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_success_get_data(self):
        """應該回應200且有資料"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/fear-and-greed/reversal-signal')
            self.assertEqual(200, res.status_code)
            self.assertEqual(4, len(res.json["data"]["signals"]))
            self.assertEqual("reverse_5", res.json["data"]["text"])
            self.assertEqual("reverse_5", res.json["data"]["signals"][0]["indicatorStatus"])
            self.assertEqual("reverse_4", res.json["data"]["signals"][1]["indicatorStatus"])
            self.assertEqual("reverse_-4", res.json["data"]["signals"][2]["indicatorStatus"])
            self.assertEqual("reverse_-5", res.json["data"]["signals"][3]["indicatorStatus"])
            self.assertEqual("2023/3/14", res.json["data"]["updatedAt"])
