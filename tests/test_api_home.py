from requests import Response

from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiHome(BaseFlaskTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_it_should_200_when_api_is_alive(self):
        """API狀態正常，應該回應200"""
        with self.app.test_client() as client:
            res: Response = client.get("/")
            self.assertEqual(200, res.status_code)
            self.assertEqual("API is alive.", res.json["message"])
