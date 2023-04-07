from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from dbmodels.user_profile.business_account import BusinessAccount
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiUserProfileBusiness(BaseFlaskTestCase):
    business_user = "business-user"
    business_plan = "Basic Yearly"
    business_account_type = "business"

    watchlist = [{"name": "test", "symbols": [], "watchlist_id": "test"}]

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.user_sql_session.add(BusinessAccount(**{
            "user_id": self.business_user,
            "password": "dummy",
            "company": "TradingValley",
            "company_code": "tv",
            "status": True,
            "plan": self.business_plan,
            "subscribed_at": "2022-11-18",
            "expire_at": "2023-11-18",
            "watchlist": self.watchlist
        }))
        self.user_sql_session.flush()

    def _clear_test_data(self):
        self.user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id == self.business_user) \
            .delete()
        self.user_sql_session.flush()
        self.cache.clear()

    def _setup_session(self, client: FlaskClient):
        with client.session_transaction() as sess:
            sess["user_id"] = self.business_user
            sess["email"] = None
            sess["account_type"] = self.business_account_type
            sess["plan"] = self.business_plan

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/users")
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_business_user_exists(self):
        """企業用戶存在，應該回應200"""
        with self.app.test_client() as client:
            self._setup_session(client)
            res: TestResponse = client.get("/user")
            self.assertEqual(200, res.status_code)
            self.assertEqual(True, res.json["data"]["subscribed"])
            self.assertEqual(self.business_plan, res.json["data"]["plan"])
            self.assertEqual(self.watchlist, res.json["data"]["watchlist"])
            self.assertEqual(self.business_account_type, res.json["data"]["accountType"])
