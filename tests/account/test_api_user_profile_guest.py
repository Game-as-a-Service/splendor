from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiUserProfileGuest(BaseFlaskTestCase):
    guest_user = None
    guest_email = None
    guest_account_type = None
    guest_plan = "Guest"

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        pass

    def _clear_test_data(self):
        pass

    def _setup_session(self, client: FlaskClient):
        with client.session_transaction() as sess:
            sess["user_id"] = self.guest_user
            sess["email"] = self.guest_email
            sess["account_type"] = self.guest_account_type
            sess["plan"] = self.guest_plan

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/users")
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_guest_but_not_header(self):
        """[Guest] 沒有 header Authorization or x-api-key，應該回應200並回覆指定的訊息"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/user")
            self.assertEqual(401, res.status_code)

    def test_it_should_200_when_guest_but_token_invalid(self):
        """[Guest] header x-api-key 無效，應該回應200並回覆指定的訊息"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/user", headers={"x-api-key": "guest"})
            self.assertEqual(200, res.status_code)
            message = {
                "return_code": -401,
                "return_msg": "AuthenticationFailed: Is not a valid token.",
                "return_data": []
            }
            self.assertEqual(message, res.json)

    def test_it_should_200_when_guest_and_header_correct_and_first_login(self):
        """[Guest] header 正確且第一次登入，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/user", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual("Guest", res.json["data"]["plan"])
            self.assertEqual(None, res.json["data"]["subscribed"])
            self.assertEqual(None, res.json["data"]["subscribedAt"])
            self.assertEqual(None, res.json["data"]["expireAt"])
            self.assertEqual(None, res.json["data"]["watchlist"])

    def test_it_should_200_when_guest_and_header_correct_and_login(self):
        """[Guest] header 正確且登入，應該回應200"""
        with self.app.test_client() as client:
            self._setup_session(client)
            res: TestResponse = client.get("/user", headers={"x-api-key": "Guest"})
            self.assertEqual(200, res.status_code)
            self.assertEqual("Guest", res.json["data"]["plan"])
            self.assertEqual(None, res.json["data"]["subscribed"])
            self.assertEqual(None, res.json["data"]["subscribedAt"])
            self.assertEqual(None, res.json["data"]["expireAt"])
            self.assertEqual(None, res.json["data"]["watchlist"])
