from werkzeug.test import TestResponse

from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiEarlyWarningHistorical(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add_all([
            HistoricalMarketIndicator(**{
                "indicator": "Market_Traffic_Light",
                "date": "2023-03-14",
                "value": 1
            }),
            HistoricalMarketIndicator(**{
                "indicator": "Market_Traffic_Light",
                "date": "2023-03-13",
                "value": 0
            }),
            HistoricalMarketIndicator(**{
                "indicator": "Market_Traffic_Light",
                "date": "2023-03-12",
                "value": -1
            }),
            HistoricalMarketIndicator(**{
                "indicator": "Market_Traffic_Light",
                "date": "2023-03-11",
                "value": 1
            }),
            HistoricalMarketIndicator(**{
                "indicator": "Market_Traffic_Light",
                "date": "2023-03-10",
                "value": -1
            }),
        ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(HistoricalMarketIndicator) \
            .filter(HistoricalMarketIndicator.indicator == "Market_Traffic_Light") \
            .delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/early-warning/recent-signal')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_success_get_data(self):
        """應該回應200且有資料"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/early-warning/recent-signals')
            self.assertEqual(200, res.status_code)
            self.assertEqual("beware", res.json["data"]["oneWeekAgo"])
            self.assertEqual("warning", res.json["data"]["twoWeekAgo"])
            self.assertEqual("stable", res.json["data"]["threeWeekAgo"])
            self.assertEqual("warning", res.json["data"]["fourWeekAgo"])
            self.assertEqual("2023/3/14", res.json["data"]["updatedAt"])
