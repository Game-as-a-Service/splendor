from datetime import date

from werkzeug.test import TestResponse

from dbmodels.nike.insider_buying_info import InsiderBuyingInfo
from tests import setup_guest_session, setup_basic_session, setup_free_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiInsiderBuyingInfo(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        month = date.today().month
        year = date.today().year
        for i in range(15):
            self.nike_sql_session.add(InsiderBuyingInfo(**{
                "symbol": "DUMMY",
                "filing_date": f"{year}-{str(month).zfill(2)}-{str(i).zfill(2)}",
                "buyer_name": "buyer",
                "buyer_title": "officer",
                "trade_date": f"{year}-{str(month).zfill(2)}-{str(i).zfill(2)}",
                "trade_num": 100,
                "trade_cash": 1000,
                "trade_num_after": 100,
                "stock_category": "normal",
                "stock_category_zh": "普通股"
            }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(InsiderBuyingInfo).filter(InsiderBuyingInfo.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/insider-buying')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，但會回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/insider-buying-info/SAMPLE/1/10")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_or_404_when_parameter_invalid(self):
        """In Path Parameter 參數錯誤，應該回應404 or 200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/insider-buying-info//1/10")
            self.assertEqual(404, res.status_code)

            setup_basic_session(client)
            res: TestResponse = client.get("/insider-buying-info/1/1/10")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_guest_and_symbol_exists_and_page_1(self):
        """[Guest] Symbol存在並且取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/insider-buying-info/DUMMY/1/10", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("lock", res.json["data"][0]["tradeNum"])
            self.assertEqual("lock", res.json["data"][0]["tradeCash"])
            self.assertEqual("lock", res.json["data"][0]["tradeNumAfter"])

    def test_it_should_200_when_free_plan_and_symbol_exists_and_page_1(self):
        """[免費方案] Symbol存在並且取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/insider-buying-info/DUMMY/1/10")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("lock", res.json["data"][0]["tradeNum"])
            self.assertEqual("lock", res.json["data"][0]["tradeCash"])
            self.assertEqual("lock", res.json["data"][0]["tradeNumAfter"])

    def test_it_should_200_when_basic_plan_and_symbol_exists_and_page_1(self):
        """[基礎方案] Symbol存在並且取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/insider-buying-info/DUMMY/1/10")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual(100, res.json["data"][0]["tradeNum"])
            self.assertEqual(1000, res.json["data"][0]["tradeCash"])
            self.assertEqual(100, res.json["data"][0]["tradeNumAfter"])

    def test_it_should_200_when_basic_plan_and_symbol_exists_and_page_2(self):
        """[基礎方案] Symbol存在並且取第二頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/insider-buying-info/DUMMY/2/10")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json["data"]))

    def test_it_should_200_when_business_plan_and_symbol_exists_and_page_1(self):
        """[企業方案] Symbol存在並且取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/insider-buying-info/DUMMY/1/10")
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual(100, res.json["data"][0]["tradeNum"])
            self.assertEqual(1000, res.json["data"][0]["tradeCash"])
            self.assertEqual(100, res.json["data"][0]["tradeNumAfter"])
