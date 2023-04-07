from werkzeug.test import TestResponse

from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiFearAndGreedHistorical(BaseFlaskTestCase):

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
                "indicator": "fear_and_greed_indicator",
                "value": 5,
                "date": "2023-03-15"
            }),
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "value": 4,
                "date": "2023-03-14"
            }),
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "value": 3,
                "date": "2023-03-13"
            }),
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "value": 2,
                "date": "2023-03-12"
            }),
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "value": 1,
                "date": "2023-03-11"
            }),
            HistoricalMarketIndicator(**{
                "indicator": "fear_and_greed_indicator",
                "value": 0,
                "date": "2023-03-10"
            })
        ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(HistoricalMarketIndicator) \
            .filter(HistoricalMarketIndicator.indicator == "fear_and_greed_indicator") \
            .delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/fear-and-greed/historical123')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_success_get_data(self):
        """應該回應200且有資料"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/market-sentiment/fear-and-greed/historical')
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json['data']['historical']))
            self.assertEqual("2023/3/15", res.json["data"]["updatedAt"])
