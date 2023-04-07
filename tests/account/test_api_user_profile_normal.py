from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from dbmodels.user_profile.nike_customer_info import NikeCustomerInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiUserProfileGuest(BaseFlaskTestCase):
    normal_user = "normal-user-id"
    normal_email = "test@email.com"
    normal_plan = "Free"
    normal_account_type = "normal"

    watchlist = [{"name": "test", "symbols": [], "watchlist_id": "test"}]

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.user_sql_session.add(NikeCustomerInfo(**{
            "user_id": self.normal_user,
            "email": self.normal_email,
            "plan": self.normal_plan,
            "status": "inactive",
            "watchlist": self.watchlist
        }))
        self.user_sql_session.flush()

    def _clear_test_data(self):
        self.user_sql_session.query(NikeCustomerInfo) \
            .filter(NikeCustomerInfo.user_id == self.normal_user) \
            .delete()
        self.user_sql_session.flush()
        self.cache.clear()

    def _setup_session(self, client: FlaskClient):
        with client.session_transaction() as sess:
            sess["user_id"] = self.normal_user
            sess["email"] = self.normal_email
            sess["account_type"] = self.normal_account_type
            sess["plan"] = self.normal_plan

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/users")
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_normal_user_exists(self):
        """一般用戶存在，應該回應200"""
        with self.app.test_client() as client:
            self._setup_session(client)
            res: TestResponse = client.get("/user")
            self.assertEqual(200, res.status_code)
            self.assertEqual(False, res.json["data"]["subscribed"])
            self.assertEqual(self.normal_plan, res.json["data"]["plan"])
            self.assertEqual(None, res.json["data"]["subscribedAt"])
            self.assertEqual(None, res.json["data"]["expireAt"])
            self.assertEqual(self.watchlist, res.json["data"]["watchlist"])
            self.assertEqual(self.normal_account_type, res.json["data"]["accountType"])
