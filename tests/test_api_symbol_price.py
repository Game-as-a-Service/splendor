from werkzeug.test import TestResponse

from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolPrice(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        stm = """
            INSERT INTO
                history_bar(symbol, time, time_frame, close_price)
            VALUES
                ("TEST", "2022-06-01", "D", 1.1),
                ("TEST", "2022-06-02", "D", 2.2),
                ("TEST", "2022-06-03", "D", 3.3),
                ("TEST", "2022-06-04", "D", 4.4),
                ("TEST", "2022-06-05", "D", 5.5),
                ("TEST", "2022-06-06", "D", 6.6);
        """
        self.symbol_sql_session.execute(stm)
        self.symbol_sql_session.flush()

    def _clear_test_data(self):
        stm = """
            DELETE FROM
                history_bar
            WHERE
                symbol = "TEST";
        """
        self.symbol_sql_session.execute(stm)
        self.symbol_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/symbol/prices/TEST/2022-06-01/2022-06-02')
            self.assertEqual(404, res.status_code)

    def test_it_should_409_when_permission_invalid(self):
        """用戶權限不足，應該回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/symbol/price/TEST1/2022-06-01/2022-06-02')
            self.assertEqual(409, res.status_code)

            setup_free_session(client)
            res: TestResponse = client.get('/symbol/price/TEST1/2022-06-01/2022-06-02')
            self.assertEqual(409, res.status_code)

    def test_it_should_200_when_not_find_symbol(self):
        """沒有搜尋到指定的Symbol，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get('/symbol/price/TEST1/2022-06-01/2022-06-02')
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_find_symbol(self):
        """有搜尋到指定的Symbol，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get('/symbol/price/TEST/2022-06-01/2022-06-02')
            self.assertEqual(200, res.status_code)
            self.assertNotEqual([], res.json["data"])
            self.assertEqual(2, len(res.json["data"]))

    def test_it_should_200_when_find_symbol_but_not_in_datetime_range(self):
        """有搜尋到指定的Symbol，但指定的時間範圍內無資料，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get('/symbol/price/TEST/2022-06-07/2022-06-08')
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])
