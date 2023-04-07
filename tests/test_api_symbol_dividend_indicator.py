from werkzeug.test import TestResponse

from dbmodels.nike.symbol_dividend_info import SymbolDividendInfo
from dbmodels.nike.symbol_info import SymbolInfo
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolDividendIndicator(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add(SymbolInfo(**{
            "symbol": "DUMMY",
            "name": "DUMMY",
            "country": "US",
            "price": 100.12,
            "main_category": "main",
            "main_category_id": "main",
            "sub_category": "sub",
            "sub_category_id": "sub"
        }))
        self.nike_sql_session.add_all([
            SymbolDividendInfo(**{
                "symbol": "DUMMY",
                "dividend_yield": 5.5,
                "filled_days": 5.5,
                "filled_ratio": 5.5,
                "volatility": 5.5
            }),
            SymbolDividendInfo(**{
                "symbol": "main",
                "dividend_yield": 4.4,
                "filled_days": 4.4,
                "filled_ratio": 4.4,
                "volatility": 4.4
            }),
        ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.symbol == "DUMMY").delete()
        self.nike_sql_session.query(SymbolDividendInfo).filter(
            SymbolDividendInfo.symbol.in_(["DUMMY", "main"])).delete()
        self.nike_sql_session.flush()

        self.cache.clear()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/dividend/SAMPLE')
            self.assertEqual(404, res.status_code)

    def test_it_should_404_when_symbol_not_found(self):
        """找不到Symbol，應該回應404"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/dividend-indicator/SAMPLE')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_guest_and_symbol_is_exists(self):
        """[Guest] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/dividend-indicator/DUMMY", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual("lock", res.json["data"]["symbol"]["filledDays"])
            self.assertEqual("lock", res.json["data"]["symbol"]["filledRatio"])

    def test_it_should_200_when_free_plan_and_symbol_is_exists(self):
        """[免費方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/dividend-indicator/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual("lock", res.json["data"]["symbol"]["filledDays"])
            self.assertEqual("lock", res.json["data"]["symbol"]["filledRatio"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists(self):
        """[基礎方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/dividend-indicator/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5.5, res.json["data"]["symbol"]["filledDays"])
            self.assertEqual(5.5, res.json["data"]["symbol"]["filledRatio"])

    def test_it_should_200_when_business_plan_and_symbol_is_exists(self):
        """[企業方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/dividend-indicator/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5.5, res.json["data"]["symbol"]["filledDays"])
            self.assertEqual(5.5, res.json["data"]["symbol"]["filledRatio"])
