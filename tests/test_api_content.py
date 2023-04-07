from requests import Response

from dbmodels.nike.description import Description
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiContent(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add(Description(**{
            "symbol": "DUMMY",
            "oriented": "value",
            "info": "5_to_1",
            "description": "Hello."
        }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(Description).filter(Description.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: Response = client.get('/contents')
            self.assertEqual(404, res.status_code)

    def test_it_should_404_when_parameter_invalid(self):
        """Payload參數錯誤，應該回應422"""
        with self.app.test_client() as client:
            res: Response = client.get("/content//value/4_to_3")
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，但會回應200"""
        with self.app.test_client() as client:
            res: Response = client.get('/content/SAMPLE/value/5_to_1')
            self.assertEqual(200, res.status_code)
            self.assertEqual("", res.json["data"]["content"])

            res: Response = client.get("/content/1/value/4_to_3")
            self.assertEqual(200, res.status_code)
            self.assertEqual("", res.json["data"]["content"])

            res: Response = client.get("/content/DUMMY/1/4_to_3")
            self.assertEqual(200, res.status_code)
            self.assertEqual("", res.json["data"]["content"])

    def test_it_should_200_when_symbol_is_exsits(self):
        """Symbol 存在，應該回應200"""
        with self.app.test_client() as client:
            res: Response = client.get('/content/DUMMY/value/5_to_1')
            self.assertEqual(200, res.status_code)
            self.assertEqual("Hello.", res.json["data"]["content"])
