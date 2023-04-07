from werkzeug.test import TestResponse

from dbmodels.nike.symbol_info import SymbolInfo
from tests import setup_guest_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolsScore(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self) -> None:
        self.nike_sql_session.add(
            SymbolInfo(**{
                "symbol": "D",
                "name": "D",
                "country": "US",
                "price": 100.12,
                "value": 1,
                "trend": 2,
                "swing": 3,
                "dividend": 4,
                "chip": 5,
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            })
        )
        self.nike_sql_session.add(
            SymbolInfo(**{
                "symbol": "DU",
                "name": "DU",
                "country": "US",
                "price": 100.12,
                "value": 1,
                "trend": 2,
                "swing": 3,
                "dividend": 4,
                "chip": 5,
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            })
        )
        self.nike_sql_session.add(
            SymbolInfo(**{
                "symbol": "DUMMY",
                "name": "DUMMY",
                "country": "US",
                "price": 100.12,
                "value": 1,
                "trend": 2,
                "swing": 3,
                "dividend": 4,
                "chip": 5,
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            })
        )
        self.nike_sql_session.flush()

    def _clear_test_data(self) -> None:
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.symbol.in_(["D", "DU", "DUMMY"])).delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.post('/symbol/scores')
            self.assertEqual(404, res.status_code)

    def test_it_should_409_when_permission_invalid(self):
        """用戶權限不足，應該回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.post('/symbol/score', json={"symbolList": ["D", "DU"]})
            self.assertEqual(409, res.status_code)

    def test_it_should_422_when_payload_not_correct(self):
        """Payload錯誤，應該回應422"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.post('/symbol/score', json={})
            self.assertEqual(422, res.status_code)

    def test_it_should_200_when_payload_is_correct_1(self):
        """Payload正確，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.post('/symbol/score', json={"symbolList": ["D", "DU"]})
            self.assertEqual(200, res.status_code)
            data = {
                "D": {"value": 1, "trend": 2, "swing": 3, "dividend": 4, "chip": 5},
                "DU": {"value": 1, "trend": 2, "swing": 3, "dividend": 4, "chip": 5},
            }
            self.assertEqual(data, res.json["data"])

    def test_it_should_200_when_payload_is_correct_2(self):
        """Payload正確，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.post('/symbol/score', json={"symbolList": ["D", "DU", "DUMMY"]})
            self.assertEqual(200, res.status_code)
            data = {
                "D": {"value": 1, "trend": 2, "swing": 3, "dividend": 4, "chip": 5},
                "DU": {"value": 1, "trend": 2, "swing": 3, "dividend": 4, "chip": 5},
                "DUMMY": {"value": 1, "trend": 2, "swing": 3, "dividend": 4, "chip": 5},
            }
            self.assertEqual(data, res.json["data"])
