from werkzeug.test import TestResponse

from dbmodels.sec13.sec_form_13f import SECForm13F
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiInvestorRanking(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        for i in range(11):
            self.sec13f_sql_session.add(
                SECForm13F(**{
                    "ticker": "DUMMY",
                    "investorname": i,
                    "securitytype": "SHR",
                    "calendardate": "2022-03-31",
                    "value": i,
                    "units": i,
                    "price": i,
                    "style": "G",
                    "weight_pct": i,
                    "investorname_alt": i,
                    "units_pct": i
                }))
        self.sec13f_sql_session.flush()

    def _clear_test_data(self):
        self.sec13f_sql_session.query(SECForm13F).filter(SECForm13F.ticker == "DUMMY").delete()
        self.sec13f_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/investor-rankings/TSLA/1/10')
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_page_set_0(self):
        """Page參數為0，應該回應400"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/investor-ranking/Dummy/0/10')
            self.assertEqual(400, res.status_code)

    def test_it_should_200_when_symbol_not_exists(self):
        """Symbol不存在，應該回應200"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/investor-ranking/Dummy-1/1/10')
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])
            self.assertEqual("2022 Q1", res.json["quarter"])
            self.assertEqual(0, res.json["total"])
            self.assertEqual(1, res.json["page"])
            self.assertEqual(10, res.json["pageSize"])

    def test_it_should_200_when_guest_and_symbol_is_exists_and_page1(self):
        """[Guest] Symbol存在，應該回應200且page1會有10筆資料"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get('/investor-ranking/DUMMY/1/10', headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("2022 Q1", res.json["quarter"])
            self.assertEqual("2022-03-31", res.json["updatedAt"])
            self.assertEqual(11, res.json["total"])
            self.assertEqual(1, res.json["page"])
            self.assertEqual(10, res.json["pageSize"])
            self.assertEqual("lock", res.json["data"][0]["units"])
            self.assertEqual("lock", res.json["data"][0]["unitsPct"])
            self.assertEqual("lock", res.json["data"][0]["value"])
            self.assertEqual("lock", res.json["data"][0]["weightPct"])

    def test_it_should_200_when_free_plan_and_symbol_is_exists_and_page1(self):
        """[免費方案] Symbol存在，應該回應200且page1會有10筆資料"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get('/investor-ranking/DUMMY/1/10')
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("2022 Q1", res.json["quarter"])
            self.assertEqual("2022-03-31", res.json["updatedAt"])
            self.assertEqual(11, res.json["total"])
            self.assertEqual(1, res.json["page"])
            self.assertEqual(10, res.json["pageSize"])
            self.assertEqual("lock", res.json["data"][0]["units"])
            self.assertEqual("lock", res.json["data"][0]["unitsPct"])
            self.assertEqual("lock", res.json["data"][0]["value"])
            self.assertEqual("lock", res.json["data"][0]["weightPct"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists_and_page1(self):
        """[基礎方案] Symbol存在，應該回應200且page1會有10筆資料"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get('/investor-ranking/DUMMY/1/10')
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("2022 Q1", res.json["quarter"])
            self.assertEqual("2022-03-31", res.json["updatedAt"])
            self.assertEqual(11, res.json["total"])
            self.assertEqual(1, res.json["page"])
            self.assertEqual(10, res.json["pageSize"])
            self.assertEqual(0, res.json["data"][0]["units"])
            self.assertEqual(0, res.json["data"][0]["unitsPct"])
            self.assertEqual(0, res.json["data"][0]["value"])
            self.assertEqual(0, res.json["data"][0]["weightPct"])

    def test_it_should_200_when_basic_plan_and_symbol_is_exists_and_page2(self):
        """[基礎方案] Symbol存在，應該回應200且page2會有1筆資料"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get('/investor-ranking/DUMMY/2/10')
            self.assertEqual(200, res.status_code)
            self.assertEqual(1, len(res.json["data"]))
            self.assertEqual("2022 Q1", res.json["quarter"])
            self.assertEqual("2022-03-31", res.json["updatedAt"])
            self.assertEqual(11, res.json["total"])
            self.assertEqual(2, res.json["page"])
            self.assertEqual(10, res.json["pageSize"])

    def test_it_should_200_when_business_plan_and_symbol_is_exists_and_page1(self):
        """[企業方案] Symbol存在，應該回應200且page1會有10筆資料"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get('/investor-ranking/DUMMY/1/10')
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, len(res.json["data"]))
            self.assertEqual("2022 Q1", res.json["quarter"])
            self.assertEqual("2022-03-31", res.json["updatedAt"])
            self.assertEqual(11, res.json["total"])
            self.assertEqual(1, res.json["page"])
            self.assertEqual(10, res.json["pageSize"])
            self.assertEqual(0, res.json["data"][0]["units"])
            self.assertEqual(0, res.json["data"][0]["unitsPct"])
            self.assertEqual(0, res.json["data"][0]["value"])
            self.assertEqual(0, res.json["data"][0]["weightPct"])
