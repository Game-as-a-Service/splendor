from werkzeug.test import TestResponse

from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiTrendHistoricalPerformance(BaseFlaskTestCase):

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

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/historical-rating')
            self.assertEqual(404, res.status_code)
