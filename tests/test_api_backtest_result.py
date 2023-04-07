from werkzeug.test import TestResponse

from dbmodels.nike.backtest_result import BacktestResult
from dbmodels.nike.symbol_info import SymbolInfo
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiBacktestResult(BaseFlaskTestCase):
    guest_user = None
    guest_email = None
    guest_type = None
    guest_plan = "Guest"

    free_user = "free-user"
    free_mail = "free@email.com"
    free_type = "normal"
    free_plan = "Free"

    basic_user = "basic-user"
    basic_mail = "basic@email.com"
    basic_type = "normal"
    basic_plan = "Basic Yearly"

    business_user = "business-user"
    business_mail = "business@email.com"
    business_type = "business"
    business_plan = "Basic Yearly"

    watchlist = [{"name": "test", "symbols": [], "watchlist_id": "test"}]

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
            "main_category_id": "mian",
            "sub_category": "sub",
            "sub_category_id": "sub"
        }))
        self.nike_sql_session.add_all([
            BacktestResult(**{
                "symbol": "DUMMY",
                "oriented": "value",
                "version": "1.0",
                "strategy": "4_3",
                "occurrence": 2,
                "profits": 1,
                "profitability": 50.0,
                "avg_profit_and_loss": 12.1,
                "avg_profit": 12.1,
                "avg_loss": 12.1,
                "avg_profit_to_loss_ratio": 12.1,
                "quantile_25": 12.1,
                "quantile_50": 12.1,
                "quantile_75": 12.1,
                "avg_holding_time": 12.1
            }),
            BacktestResult(**{
                "symbol": "DUMMY",
                "oriented": "value",
                "version": "2.0",
                "strategy": "4_3",
                "occurrence": 2,
                "profits": 1,
                "profitability": 50.0,
                "avg_profit_and_loss": 12.1,
                "avg_profit": 12.1,
                "avg_loss": 12.1,
                "avg_profit_to_loss_ratio": 12.1,
                "quantile_25": 12.1,
                "quantile_50": 12.1,
                "quantile_75": 12.1,
                "avg_holding_time": 12.1
            }),
            BacktestResult(**{
                "symbol": "main",
                "oriented": "value",
                "version": "1.0",
                "strategy": "4_3",
                "occurrence": 2,
                "profits": 1,
                "profitability": 50.0,
                "avg_profit_and_loss": 12.1,
                "avg_profit": 12.1,
                "avg_loss": 12.1,
                "avg_profit_to_loss_ratio": 12.1,
                "quantile_25": 12.1,
                "quantile_50": 12.1,
                "quantile_75": 12.1,
                "avg_holding_time": 12.1
            }),
            BacktestResult(**{
                "symbol": "DUMMY",
                "oriented": "swing",
                "version": "1.0",
                "strategy": "4_3",
                "occurrence": 2,
                "profits": 1,
                "profitability": 50.0,
                "avg_profit_and_loss": 12.1,
                "avg_profit": 12.1,
                "avg_loss": 12.1,
                "avg_profit_to_loss_ratio": 12.1,
                "quantile_25": 12.1,
                "quantile_50": 12.1,
                "quantile_75": 12.1,
                "avg_holding_time": 12.1
            }),
            BacktestResult(**{
                "symbol": "main",
                "oriented": "swing",
                "version": "1.0",
                "strategy": "4_3",
                "occurrence": 2,
                "profits": 1,
                "profitability": 50.0,
                "avg_profit_and_loss": 12.1,
                "avg_profit": 12.1,
                "avg_loss": 12.1,
                "avg_profit_to_loss_ratio": 12.1,
                "quantile_25": 12.1,
                "quantile_50": 12.1,
                "quantile_75": 12.1,
                "avg_holding_time": 12.1
            }),
        ])
        self.nike_sql_session.flush()

        self.symbol_sql_session.execute("""
                    INSERT INTO history_bar(symbol, time, time_frame) VALUES
                    ('DUMMY', '2007-01-01', 'D'),
                    ('DUMMY', '2007-01-02', 'D'),
                    ('DUMMY', '2007-01-03', 'D');
                """)
        self.symbol_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(SymbolInfo).filter(SymbolInfo.symbol == "DUMMY").delete()
        self.nike_sql_session.query(BacktestResult).filter(BacktestResult.symbol.in_(["DUMMY", "main"])).delete()
        self.nike_sql_session.flush()
        self.symbol_sql_session.execute("""DELETE FROM history_bar WHERE symbol = 'DUMMY';""")
        self.symbol_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/backtest-resul')
            self.assertEqual(404, res.status_code)

    def test_it_should_409_when_permission_invalid(self):
        """用戶權限不足，應該回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/backtest-result/DUMMY/value/4_3")
            self.assertEqual(409, res.status_code)

            setup_free_session(client)
            res: TestResponse = client.get("/backtest-result/DUMMY/value/4_3")
            self.assertEqual(409, res.status_code)

    def test_it_should_404_when_parameter_invalid(self):
        """path參數錯誤，應該回應404"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/backtest-result/1/value/4_3")
            self.assertEqual(404, res.status_code)

            setup_business_session(client)
            res: TestResponse = client.get("/backtest-result//value/4_3")
            self.assertEqual(404, res.status_code)

            setup_business_session(client)
            res: TestResponse = client.get("/backtest-result/DUMMY/1/4_3")
            self.assertEqual(400, res.status_code)

    def test_it_should_404_when_symbol_not_found(self):
        """找不到Symbol，應該回應404"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/backtest-result/SAMPLE/value/4_3", )
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_exists(self):
        """path正確且symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/backtest-result/DUMMY/value/4_3")
            self.assertEqual(200, res.status_code)
            self.assertIsNotNone(res.json["data"])

            setup_business_session(client)
            res: TestResponse = client.get("/backtest-result/DUMMY/swing/4_3")
            self.assertEqual(200, res.status_code)
            self.assertIsNotNone(res.json["data"])
