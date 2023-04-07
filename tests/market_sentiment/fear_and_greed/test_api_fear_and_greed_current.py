from werkzeug.test import TestResponse

from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from dbmodels.nike.market_indicator_current_state import MarketIndicatorCurrentState
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiFearAndGreedCurrent(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add(
            MarketIndicatorCurrentState(**{
                "indicator": "fear_and_greed_indicator",
                "value": 4,
                "description": "greed"
            }))
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
        self.nike_sql_session.query(MarketIndicatorCurrentState) \
            .filter(MarketIndicatorCurrentState.indicator == 'fear_and_greed_indicator') \
            .delete()
        self.nike_sql_session.query(HistoricalMarketIndicator) \
            .filter(HistoricalMarketIndicator.indicator == "fear_and_greed_indicator") \
            .delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/fear-and-greed/current123')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_success_get_data(self):
        """應該回應200且有資料"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/fear-and-greed/current')
            self.assertEqual(200, res.status_code)
            self.assertEqual("reverse_5", res.json["data"]["text"])
            self.assertEqual(4, res.json["data"]["score"])
            self.assertEqual("greed", res.json["data"]["description"])
            self.assertEqual("2023/3/14", res.json["data"]["updatedAt"])
