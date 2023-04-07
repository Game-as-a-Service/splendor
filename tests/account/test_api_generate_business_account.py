import hashlib

from requests import Response

from dbmodels.user_profile.business_account import BusinessAccount
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiGenerateBusinessAccount(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.user_sql_session.add(BusinessAccount(**{
            "user_id": "dummy-1",
            "password": "dummy",
            "company": "TradingValley",
            "company_code": "tv",
            "status": True,
            "plan": "Basic Yearly",
            "subscribed_at": "2022-11-18",
            "expire_at": "2023-11-18",
            "watchlist": []
        }))
        self.user_sql_session.flush()

    def _clear_test_data(self):
        self.user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id.in_(["test-user-id", "dummy-1"])) \
            .delete()
        self.user_sql_session.flush()
        self.cache.clear()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: Response = client.post('/businesss/generate/user', json={})
            self.assertEqual(404, res.status_code)

    def test_it_should_422_when_payload_is_wrong(self):
        """payload有誤，應該回應422"""
        with self.app.test_client() as client:
            payload = {
                "usernae": "test-user-id",
                "password": "test",
                "company": "TradingValley",
                "companyCode": "tv",
                "plan": "Basic Yearly",
                "subscribedAt": "2022-11-18",
                "expireAt": "2023-11-18"
            }
            res: Response = client.post('/business/generate/user', json=payload)
            self.assertEqual(422, res.status_code)

    def test_it_should_400_when_user_is_exists(self):
        """用戶已存在，應該回應400"""
        with self.app.test_client() as client:
            payload = {
                "username": "dummy-1",
                "password": "test",
                "company": "TradingValley",
                "companyCode": "tv",
                "plan": "Basic Yearly",
                "subscribedAt": "2022-11-18",
                "expireAt": "2023-11-18"
            }
            res: Response = client.post('/business/generate/user', json=payload)
            self.assertEqual(400, res.status_code)

    def test_it_should_200_when_payload_is_correct(self):
        """payload正確，應該回應200"""
        with self.app.test_client() as client:
            payload = {
                "username": "test-user-id",
                "password": "test",
                "company": "TradingValley",
                "companyCode": "tv",
                "plan": "Basic Yearly",
                "subscribedAt": "2022-11-18",
                "expireAt": "2023-11-18"
            }
            res: Response = client.post('/business/generate/user', json=payload)
            self.assertEqual(200, res.status_code)

            business: BusinessAccount = self.user_sql_session.query(BusinessAccount) \
                .filter(BusinessAccount.user_id == "test-user-id") \
                .first()

            password = "test"
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            self.assertEqual("test-user-id", business.user_id)
            self.assertEqual(password, business.password)
            self.assertEqual("TradingValley", business.company)
            self.assertEqual("tv", business.company_code)
            self.assertEqual("Basic Yearly", business.plan)
