from werkzeug.test import TestResponse

from dbmodels.nike.recent_performance import RecentPerformance
from dbmodels.nike.symbol_info import SymbolInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolInfo(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    dummy_symbol_info = {
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
    }

    dummy_recent_performance = [
        {
            "symbol": "DUMMY",
            "_1d_return": 100.2,
            "_5d_return": 110.2,
            "_1m_return": 120.2,
            "_3m_return": 130.2,
            "_6m_return": 140.2,
            "_1y_return": 150.2
        },
        {
            "symbol": "main",
            "_1d_return": 100.2,
            "_5d_return": 110.2,
            "_1m_return": 120.2,
            "_3m_return": 130.2,
            "_6m_return": 140.2,
            "_1y_return": 150.2
        },
    ]

    def _prepare_test_data(self):
        self.nike_sql_session.add(SymbolInfo(**self.dummy_symbol_info))
        for i in self.dummy_recent_performance:
            self.nike_sql_session.add(RecentPerformance(**i))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.symbol == self.dummy_symbol_info["symbol"]).delete()
        for i in self.dummy_recent_performance:
            self.nike_sql_session.query(RecentPerformance).filter(RecentPerformance.symbol == i["symbol"]).delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/symbol')
            self.assertEqual(404, res.status_code)

    def test_it_should_404_when_symbol_not_found(self):
        """找不到Symbol，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/symbol-info/SAMPLE")
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_is_exists(self):
        """Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/symbol-info/DUMMY")
            self.assertEqual(200, res.status_code)
