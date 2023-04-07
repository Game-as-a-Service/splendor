from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiUserProfile(BaseFlaskTestCase):
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
