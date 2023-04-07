from werkzeug.test import TestResponse

from dbmodels.nike.symbol_info import SymbolInfo
from dbmodels.nike.top10_related_symbol import Top10RelatedSymbol
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiRelatedSymbol(BaseFlaskTestCase):

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
            "value": 1,
            "trend": 2,
            "swing": 3,
            "dividend": 4,
            "chip": 5,
            "market_cap": 123.45,
            "main_category": "main",
            "main_category_id": "main",
            "sub_category": "sub",
            "sub_category_id": "sub"
        }))
        for i in range(10):
            self.nike_sql_session.add(SymbolInfo(**{
                "symbol": f"DUMMY-{i}",
                "name": f"DUMMY-{i}",
                "country": "US",
                "price": 100.12,
                "value": 1,
                "trend": 2,
                "swing": 3,
                "dividend": 4,
                "chip": 5,
                "market_cap": 123.45,
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }))
            self.nike_sql_session.add(Top10RelatedSymbol(**{
                "symbol": "DUMMY",
                "related_symbol": f"DUMMY-{i}",
                "correlation": 9.0
            }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.symbol == "DUMMY").delete()
        self.nike_sql_session.query(Top10RelatedSymbol).filter(Top10RelatedSymbol.symbol == "DUMMY").delete()
        for i in range(10):
            self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.symbol == f"DUMMY-{i}").delete()
        self.nike_sql_session.flush()

        self.cache.clear()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/related')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/related-symbol/SAMPLE")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_guest_and_symbol_is_exists(self):
        """[Guest] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/related-symbol/DUMMY", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("DUMMY-2", res.json["data"][2]["symbol"])
            self.assertEqual(9.0, res.json["data"][2]["correlation"])
            self.assertEqual("lock", res.json["data"][3]["symbol"])
            self.assertEqual("lock", res.json["data"][3]["correlation"])

    def test_it_should_200_when_free_plan_and_symbol_is_exists(self):
        """[免費方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/related-symbol/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("DUMMY-2", res.json["data"][2]["symbol"])
            self.assertEqual(9.0, res.json["data"][2]["correlation"])
            self.assertEqual("lock", res.json["data"][3]["symbol"])
            self.assertEqual("lock", res.json["data"][3]["correlation"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists(self):
        """[基礎方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/related-symbol/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("DUMMY-2", res.json["data"][2]["symbol"])
            self.assertEqual(9.0, res.json["data"][2]["correlation"])
            self.assertEqual("DUMMY-3", res.json["data"][3]["symbol"])
            self.assertEqual(9.0, res.json["data"][3]["correlation"])

    def test_it_should_200_when_business_plan_and_symbol_is_exists(self):
        """[企業方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/related-symbol/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("DUMMY-2", res.json["data"][2]["symbol"])
            self.assertEqual(9.0, res.json["data"][2]["correlation"])
            self.assertEqual("DUMMY-3", res.json["data"][3]["symbol"])
            self.assertEqual(9.0, res.json["data"][3]["correlation"])
