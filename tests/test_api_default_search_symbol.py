from flask import Response

from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiDefaultSearchSymbol(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: Response = client.get('/default/search/symbols')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_url_is_correct(self):
        """URL正確，應該回應200"""
        with self.app.test_client() as client:
            res: Response = client.get('/default/search/symbol')
            self.assertEqual(200, res.status_code)
