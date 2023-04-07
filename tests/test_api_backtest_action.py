from werkzeug.test import TestResponse

from dbmodels.nike.buy_and_sell_date import BuyAndSellDate
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiBacktestAction(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add_all([
            BuyAndSellDate(**{
                "symbol": "DUMMY",
                "oriented": "value",
                "date": "2022-06-20",
                "strategy": "4_to_3",
                "action": "BUY"
            }),
            BuyAndSellDate(**{
                "symbol": "DUMMY",
                "oriented": "value",
                "date": "2022-06-21",
                "strategy": "4_to_3",
                "action": "SELL"
            }),
            BuyAndSellDate(**{
                "symbol": "DUMMY",
                "oriented": "value",
                "date": "2022-06-22",
                "strategy": "5_to_1",
                "action": "BUY"
            }),
            BuyAndSellDate(**{
                "symbol": "DUMMY",
                "oriented": "value",
                "date": "2022-06-20",
                "strategy": "5_to_1",
                "action": "SELL"
            }),
        ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(BuyAndSellDate).filter(BuyAndSellDate.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()
        self.cache.clear()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/backtest-actio')
            self.assertEqual(404, res.status_code)

    def test_it_should_409_when_permission_invalid(self):
        """用戶權限不足，應該回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/backtest-action/1/value/4_to_3/2022-01-01/2022-08-08")
            self.assertEqual(409, res.status_code)

            setup_free_session(client)
            res: TestResponse = client.get("/backtest-action/1/value/4_to_3/2022-01-01/2022-08-08")
            self.assertEqual(409, res.status_code)

    def test_it_should_200_or_404_when_parameter_invalid_and_empty_data(self):
        """參數錯誤或無資料時，應該回應200 or 404"""
        with self.app.test_client() as client:
            setup_basic_session(client)

            res: TestResponse = client.get("/backtest-action/1/value/4_to_3/2022-01-01/2022-08-08")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

            res: TestResponse = client.get("/backtest-action//oriented/strategy")
            self.assertEqual(404, res.status_code)

            res: TestResponse = client.get("/backtest-action/DUMMY/1/4_to_3/2022-01-01/2022-08-08")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_symbol_not_exists(self):
        """Symbol不存在，但應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/backtest-action/SAMPLE/value/4_to_3/2022-01-01/2022-08-08")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_symbol_exists(self):
        """Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/backtest-action/DUMMY/value/4_to_3/2022-01-01/2022-08-08")
            self.assertEqual(200, res.status_code)
            predict_data = [{"date": "2022-06-20", "action": "BUY"}, {"date": "2022-06-21", "action": "SELL"}]
            self.assertEqual(predict_data, res.json["data"])

            setup_business_session(client)
            res: TestResponse = client.get("/backtest-action/DUMMY/value/5_to_1/2022-01-01/2022-08-08")
            self.assertEqual(200, res.status_code)
            predict_data = [{"date": "2022-06-20", "action": "SELL"}, {"date": "2022-06-22", "action": "BUY"}]
            self.assertEqual(predict_data, res.json["data"])
