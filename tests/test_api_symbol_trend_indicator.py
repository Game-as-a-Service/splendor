from datetime import datetime

from dateutil.relativedelta import relativedelta
from werkzeug.test import TestResponse

from dbmodels.nike.indicator_result import IndicatorResult
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolTrendIndicator(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        for i in range(30):
            self.nike_sql_session.add(IndicatorResult(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(days=i),
                "indicator": "power_squeeze_daily",
                "value": i + 1
            }))
            self.nike_sql_session.add(IndicatorResult(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(days=i),
                "indicator": "power_squeeze_mom_daily",
                "value": i + 1
            }))
            self.nike_sql_session.add(IndicatorResult(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(days=i),
                "indicator": "surfing_trend_daily",
                "value": i + 1
            }))
        for i in range(52):
            self.nike_sql_session.add(IndicatorResult(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(days=i),
                "indicator": "power_squeeze_weekly",
                "value": i + 1
            }))
            self.nike_sql_session.add(IndicatorResult(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(days=i),
                "indicator": "power_squeeze_mom_weekly",
                "value": i + 1
            }))
            self.nike_sql_session.add(IndicatorResult(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(days=i),
                "indicator": "surfing_trend_weekly",
                "value": i + 1
            }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(IndicatorResult).filter(IndicatorResult.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/trend/SAMPLE')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，但應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/trend-indicator/SAMPLE')
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"]["powerSqueezeDaily"])
            self.assertEqual([], res.json["data"]["powerSqueezeMomDaily"])
            self.assertEqual([], res.json["data"]["surfingTrendDaily"])
            self.assertEqual([], res.json["data"]["powerSqueezeWeekly"])
            self.assertEqual([], res.json["data"]["powerSqueezeMomWeekly"])
            self.assertEqual([], res.json["data"]["surfingTrendWeekly"])
            self.assertEqual(None, res.json["data"]["updatedAt"])

    def test_it_should_200_when_symbol_is_exists(self):
        """Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/trend-indicator/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(30, len(res.json["data"]["powerSqueezeDaily"]))
            self.assertEqual(30, len(res.json["data"]["powerSqueezeMomDaily"]))
            self.assertEqual(30, len(res.json["data"]["surfingTrendDaily"]))
            self.assertEqual(52, len(res.json["data"]["powerSqueezeWeekly"]))
            self.assertEqual(52, len(res.json["data"]["powerSqueezeMomWeekly"]))
            self.assertEqual(52, len(res.json["data"]["surfingTrendWeekly"]))
