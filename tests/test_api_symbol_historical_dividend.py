from werkzeug.test import TestResponse

from dbmodels.nike.symbol_historical_dividend_info import SymbolHistoricalDividendInfo
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolHistoricalDividend(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        for i in range(10):
            self.nike_sql_session.add(SymbolHistoricalDividendInfo(**{
                "symbol": "DUMMY",
                "year": 2011 + i,
                "cash_dividend": 1.1,
                "stock_dividend": 2.2,
                "total_dividend": 3.3,
                "filled_days": 4,
                "dividend_yield": 5.5,
                "eps": 6.6,
                "payout_ratio": 7.7
            }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolHistoricalDividendInfo) \
            .filter(SymbolHistoricalDividendInfo.symbol == "DUMMY") \
            .delete()
        self.nike_sql_session.flush()

        self.cache.clear()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/historical/SAMPLE')
            self.assertEqual(404, res.status_code)

    def test_it_should_404_when_symbol_not_found(self):
        """找不到Symbol，應該回應404"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/historical-dividend/SAMPLE/1', headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(True, res.json["data"]["isEmpty"])
            self.assertEqual([], res.json["data"]["dividendInfo"])

    def test_it_should_200_when_guest_and_symbol_is_exists_and_get_all_data(self):
        """[Guest] Symbol存在且全拿，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/historical-dividend/DUMMY/0", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]["dividendInfo"]))
            self.assertEqual("lock", res.json["data"]["dividendInfo"][0]["filledDays"])
            self.assertEqual(False, res.json["data"]["isEmpty"])

    def test_it_should_200_when_free_plan_and_symbol_is_exists_and_get_all_data(self):
        """[免費方案] Symbol存在且全拿，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/historical-dividend/DUMMY/0")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]["dividendInfo"]))
            self.assertEqual("lock", res.json["data"]["dividendInfo"][0]["filledDays"])
            self.assertEqual(False, res.json["data"]["isEmpty"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists_and_get_all_data(self):
        """[基礎方案] Symbol存在且全拿，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/historical-dividend/DUMMY/0")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]["dividendInfo"]))
            self.assertEqual(4, res.json["data"]["dividendInfo"][0]["filledDays"])
            self.assertEqual(False, res.json["data"]["isEmpty"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists_and_only_get_3_counts(self):
        """[基礎方案] Symbol存在且只拿三筆資料，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/historical-dividend/DUMMY/3")
            self.assertEqual(200, res.status_code)
            self.assertEqual(3, len(res.json["data"]["dividendInfo"]))
            self.assertEqual(False, res.json["data"]["isEmpty"])

    def test_it_should_200_when_business_plan_and_symbol_is_exists_and_only_get_5_counts(self):
        """[企業方案] Symbol存在且只拿五筆資料，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/historical-dividend/DUMMY/5")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json["data"]["dividendInfo"]))
            self.assertEqual(False, res.json["data"]["isEmpty"])
