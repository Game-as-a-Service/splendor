from datetime import datetime

from werkzeug.test import TestResponse

from dbmodels.nike.famous_investor_status import FamousInvestorStatus
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiFamousInvestorRanking(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add(FamousInvestorStatus(**{
            "symbol": "DUMMY",
            "investorname": "DUMMY-investor",
            "investorname_zh": "DUMMY-investor-zh",
            "quarter_1": "2022-06-30",
            "units_1": "-",
            "units_pct_1": "清倉",
            "quarter_2": "2022-03-31",
            "units_2": "128959.0",
            "units_pct_2": "建倉",
            "quarter_3": "2021-12-31",
            "units_3": "-",
            "units_pct_3": "-",
            "quarter_4": "2021-09-30",
            "units_4": "-",
            "units_pct_4": "清倉",
        }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(FamousInvestorStatus) \
            .filter(FamousInvestorStatus.symbol == "DUMMY") \
            .delete()
        self.nike_sql_session.flush()
        self.cache.clear()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/famous-investor-statuss/TSLA')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_guest_header_not_correct(self):
        """Guest Header 錯誤，應該回應200且回傳指定的內容"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/famous-investor-status/TSLA', headers={"x-api-key": "error"})
            self.assertEqual(200, res.status_code)
            message = {
                "return_code": -401,
                "return_msg": "AuthenticationFailed: Is not a valid token.",
                "return_data": []
            }
            self.assertEqual(message, res.json)

    def test_it_should_200_when_symbol_not_exists(self):
        """Symbol不存在，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/famous-investor-status/TSLA')
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["fourQuarters"])
            self.assertEqual(datetime.now().strftime("%Y-%m-%d"), res.json["updatedAt"])
            self.assertEqual([], res.json["data"])

    def test_it_should_200_when_guest_and_symbol_is_exists(self):
        """[Guest] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/famous-investor-status/DUMMY', headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(["2022 Q2", "2022 Q1", "2021 Q4", "2021 Q3"], res.json["fourQuarters"])
            self.assertEqual(datetime.now().strftime("%Y-%m-%d"), res.json["updatedAt"])
            self.assertEqual([
                [
                    {"investorname": "DUMMY-investor", "investornameZh": "DUMMY-investor-zh"},
                    {"units": "lock", "unitsPct": "lock"},
                    {"units": "lock", "unitsPct": "lock"},
                    {"units": "-", "unitsPct": "-"},
                    {"units": "-", "unitsPct": "清倉"}
                ]
            ], res.json["data"])

    def test_it_should_200_when_free_plan_and_symbol_is_exists(self):
        """[免費方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get('/famous-investor-status/DUMMY')
            self.assertEqual(200, res.status_code)
            self.assertEqual(["2022 Q2", "2022 Q1", "2021 Q4", "2021 Q3"], res.json["fourQuarters"])
            self.assertEqual(datetime.now().strftime("%Y-%m-%d"), res.json["updatedAt"])
            self.assertEqual([
                [
                    {"investorname": "DUMMY-investor", "investornameZh": "DUMMY-investor-zh"},
                    {"units": "lock", "unitsPct": "lock"},
                    {"units": "lock", "unitsPct": "lock"},
                    {"units": "-", "unitsPct": "-"},
                    {"units": "-", "unitsPct": "清倉"}
                ]
            ], res.json["data"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists(self):
        """[基礎方案] Symbol存在，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get('/famous-investor-status/DUMMY')
            self.assertEqual(200, res.status_code)
            self.assertEqual(["2022 Q2", "2022 Q1", "2021 Q4", "2021 Q3"], res.json["fourQuarters"])
            self.assertEqual(datetime.now().strftime("%Y-%m-%d"), res.json["updatedAt"])
            self.assertEqual([
                [
                    {"investorname": "DUMMY-investor", "investornameZh": "DUMMY-investor-zh"},
                    {"units": "-", "unitsPct": "清倉"},
                    {"units": 128959.0, "unitsPct": "建倉"},
                    {"units": "-", "unitsPct": "-"},
                    {"units": "-", "unitsPct": "清倉"}
                ]
            ], res.json["data"])

    def test_it_should_200_when_business_plan_and_symbol_is_exists(self):
        """[企業方案] Symbol 存在，應該回應 200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get('/famous-investor-status/DUMMY')
            self.assertEqual(200, res.status_code)
            self.assertEqual(["2022 Q2", "2022 Q1", "2021 Q4", "2021 Q3"], res.json["fourQuarters"])
            self.assertEqual(datetime.now().strftime("%Y-%m-%d"), res.json["updatedAt"])
            self.assertEqual([
                [
                    {"investorname": "DUMMY-investor", "investornameZh": "DUMMY-investor-zh"},
                    {"units": "-", "unitsPct": "清倉"},
                    {"units": 128959.0, "unitsPct": "建倉"},
                    {"units": "-", "unitsPct": "-"},
                    {"units": "-", "unitsPct": "清倉"}
                ]
            ], res.json["data"])
