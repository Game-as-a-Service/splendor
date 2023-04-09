from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from dbmodels.user_profile.user_info import UserInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiUserProfile(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.user_sql_session.add(
            UserInfo(
                **{
                    "user_id": "test1",
                    "name": "test",
                }
            )
        )
        self.user_sql_session.flush()

    def _clear_test_data(self):
        self.user_sql_session.query(UserInfo).filter(
            UserInfo.user_id == "test1"
        ).delete()
        self.user_sql_session.flush()
        self.cache.clear()

    def _setup_session(self, client: FlaskClient):
        with client.session_transaction() as sess:
            pass

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/users")
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_user_exists(self):
        """一般用戶存在，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/user?userId=test1")
            self.assertEqual(200, res.status_code)
