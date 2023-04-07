from werkzeug.test import TestResponse

from dbmodels.nike.stock_mining_service import StockMiningService
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiStockMiningServiceStatus(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _clear_test_data(self):
        self.nike_sql_session.query(StockMiningService).filter(StockMiningService.service == "dummy-open").delete()
        self.nike_sql_session.query(StockMiningService).filter(StockMiningService.service == "dummy-close").delete()
        self.nike_sql_session.flush()

    def _prepare_test_data(self):
        self.nike_sql_session.add(StockMiningService(**{
            "service": "dummy-open",
            "activity": "新功能",
            "is_free_open": True,
            "open_at": "2022-10-17",
            "close_at": "2022-11-02"
        }))
        self.nike_sql_session.add(StockMiningService(**{
            "service": "dummy-close",
            "activity": "付費功能",
            "is_free_open": False,
            "open_at": None,
            "close_at": None
        }))
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/stock-mining-services/dummy')
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_service_not_exist(self):
        """請求的Service不存在，應該回應400"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/stock-mining-service/dummy')
            self.assertEqual(400, res.status_code)

    def test_it_should_200_when_service_is_exist(self):
        """請求的Service存在應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/stock-mining-service/dummy-open')
            self.assertEqual(200, res.status_code)
            self.assertEqual(True, res.json["data"]["isFreeOpen"])
            self.assertEqual("2022-10-17", res.json["data"]["openAt"])
            self.assertEqual("2022-11-02", res.json["data"]["closeAt"])

            res: TestResponse = client.get('/stock-mining-service/dummy-close')
            self.assertEqual(200, res.status_code)
            self.assertEqual(False, res.json["data"]["isFreeOpen"])
            self.assertEqual(None, res.json["data"]["openAt"])
            self.assertEqual(None, res.json["data"]["closeAt"])
