from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from dbmodels.user_profile.user_info import NikeCustomerInfo
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

