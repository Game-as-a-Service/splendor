from werkzeug.test import TestResponse

from api.biz.symbol import SECTOR
from dbmodels.nike.symbol_info import SymbolInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiAiSectorOptional(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        i = 0
        for s in SECTOR:
            i += 1
            self.nike_sql_session.add_all([
                SymbolInfo(**{
                    "symbol": f"A{i}",
                    "name": f"A{i}",
                    "country": "USA",
                    "price": 1.1,
                    "value": 1,
                    "main_category": s,
                    "main_category_zh_tw": s
                }),
                SymbolInfo(**{
                    "symbol": f"B{i}",
                    "name": f"B{i}",
                    "country": "USA",
                    "price": 2.2,
                    "value": 2,
                    "main_category": s,
                    "main_category_zh_tw": s
                })
            ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.main_category.in_(SECTOR)).delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/official-website/ai-sector-optionals/value')
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_request_invalid(self):
        """參數錯誤，應該回應400"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/official-website/ai-sector-optional/123')
            self.assertEqual(400, res.status_code)

    def test_it_should_200_when_request_valid(self):
        """參數正確，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/official-website/ai-sector-optional/value')
            self.assertEqual(200, res.status_code)
