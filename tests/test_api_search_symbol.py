from werkzeug.test import TestResponse

from dbmodels.nike.symbol_info import SymbolInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSearchSymbol(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add_all([
            SymbolInfo(**{
                "symbol": "A",
                "price": 1230000.45,
                "name": "A",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
            SymbolInfo(**{
                "symbol": "AB",
                "price": 1230000.45,
                "name": "AB",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
            SymbolInfo(**{
                "symbol": "AC",
                "price": 1230000.45,
                "name": "AC",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
            SymbolInfo(**{
                "symbol": "ABC",
                "price": 1230000.45,
                "name": "ABC",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
            SymbolInfo(**{
                "symbol": "B",
                "price": 1230000.45,
                "name": "B",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
            SymbolInfo(**{
                "symbol": "BA",
                "price": 1230000.45,
                "name": "BA",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
            SymbolInfo(**{
                "symbol": "BC",
                "price": 1230000.45,
                "name": "BC",
                "country": "US",
                "main_category": "main",
                "main_category_id": "main",
                "sub_category": "sub",
                "sub_category_id": "sub"
            }),
        ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.price == 1230000.45).delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/search/symbols/A')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_not_search_similar_word(self):
        """沒有搜尋到相似的文字，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/search/symbol/123')
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_search_similar_word_1(self):
        """有搜尋到相似的文字，應該回應200-1"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/search/symbol/A')
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_search_similar_word_2(self):
        """有搜尋到相似的文字，應該回應200-2"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/search/symbol/AB')
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_search_similar_word_3(self):
        """有搜尋到相似的文字，應該回應200-3"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/search/symbol/BC')
            self.assertEqual(200, res.status_code)
