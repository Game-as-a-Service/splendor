from werkzeug.test import TestResponse

from dbmodels.nike.reward_of_trend_period import RewardOfTrendPeriod
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiTrendPerformance(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add_all([
            RewardOfTrendPeriod(**{
                "symbol": "DUMMY",
                "score": 1,
                "occurrence": 10,
                "profits": 5,
                "profitability": 45
            }),
            RewardOfTrendPeriod(**{
                "symbol": "DUMMY",
                "score": 2,
                "occurrence": 10,
                "profits": 5,
                "profitability": 45
            }),
            RewardOfTrendPeriod(**{
                "symbol": "DUMMY",
                "score": 3,
                "occurrence": 10,
                "profits": 5,
                "profitability": 45
            }),
            RewardOfTrendPeriod(**{
                "symbol": "DUMMY",
                "score": 4,
                "occurrence": 10,
                "profits": 5,
                "profitability": 45
            }),
            RewardOfTrendPeriod(**{
                "symbol": "DUMMY",
                "score": 5,
                "occurrence": 10,
                "profits": 5,
                "profitability": 45
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
        self.nike_sql_session.query(RewardOfTrendPeriod).filter(RewardOfTrendPeriod.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

        self.symbol_sql_session.execute("""DELETE FROM history_bar WHERE symbol = 'DUMMY';""")
        self.symbol_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/trend-performane/DUMMY')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/trend-performance/SAMPLE")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"]["scoreList"])
            self.assertEqual(None, res.json["data"]["updatedAt"])

    def test_it_should_200_when_guest_and_symbol_is_exists(self):
        """[Guest] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/trend-performance/DUMMY", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json["data"]["scoreList"]))
            self.assertEqual("2007/01", res.json["data"]["startAt"])
            self.assertEqual("2007/01", res.json["data"]["endAt"])
            self.assertEqual(10, res.json["data"]["scoreList"][0]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][1]["occurrence"])
            self.assertEqual("lock", res.json["data"]["scoreList"][2]["occurrence"])
            self.assertEqual("lock", res.json["data"]["scoreList"][3]["occurrence"])
            self.assertEqual("lock", res.json["data"]["scoreList"][4]["occurrence"])

    def test_it_should_200_when_free_plan_and_symbol_is_exists(self):
        """[免費方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/trend-performance/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json["data"]["scoreList"]))
            self.assertEqual("2007/01", res.json["data"]["startAt"])
            self.assertEqual("2007/01", res.json["data"]["endAt"])
            self.assertEqual(10, res.json["data"]["scoreList"][0]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][1]["occurrence"])
            self.assertEqual("lock", res.json["data"]["scoreList"][2]["occurrence"])
            self.assertEqual("lock", res.json["data"]["scoreList"][3]["occurrence"])
            self.assertEqual("lock", res.json["data"]["scoreList"][4]["occurrence"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists(self):
        """[基礎方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/trend-performance/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json["data"]["scoreList"]))
            self.assertEqual("2007/01", res.json["data"]["startAt"])
            self.assertEqual("2007/01", res.json["data"]["endAt"])
            self.assertEqual(10, res.json["data"]["scoreList"][0]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][1]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][2]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][3]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][4]["occurrence"])

    def test_it_should_200_when_business_plan_and_symbol_is_exists(self):
        """[企業方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/trend-performance/DUMMY")
            self.assertEqual(200, res.status_code)
            self.assertEqual(5, len(res.json["data"]["scoreList"]))
            self.assertEqual("2007/01", res.json["data"]["startAt"])
            self.assertEqual("2007/01", res.json["data"]["endAt"])
            self.assertEqual(10, res.json["data"]["scoreList"][0]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][1]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][2]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][3]["occurrence"])
            self.assertEqual(10, res.json["data"]["scoreList"][4]["occurrence"])
