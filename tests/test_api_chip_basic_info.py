from werkzeug.test import TestResponse

from dbmodels.nike.chip_basic_info import ChipBasicInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiChipBasicInfo(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.nike_sql_session.add(ChipBasicInfo(**{
            "symbol": "DUMMY",
            "date": "2022-06-21",
            "cash_surplus": 10,
            "cash_net_in": 10,
            "cash_net_out": 20,
            "add_inst_num": 10,
            "add_total_cash": 10,
            "build_inst_num": 10,
            "build_total_cash": 10,
            "reduce_inst_num": 10,
            "reduce_total_cash": 10,
            "clean_inst_num": 10,
            "clean_total_cash": 10
        }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(ChipBasicInfo).filter(ChipBasicInfo.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/chip-basic/DUMMY')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，但會回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/chip-basic-info/SAMPLE')
            self.assertEqual(200, res.status_code)
            self.assertEqual(None, res.json["data"]["cashSurplus"])
            self.assertEqual(None, res.json["data"]["cashNetIn"])
            self.assertEqual(None, res.json["data"]["cashNetOut"])
            self.assertEqual(None, res.json["data"]["addInstNum"])
            self.assertEqual(None, res.json["data"]["addTotalCash"])
            self.assertEqual(None, res.json["data"]["buildInstNum"])
            self.assertEqual(None, res.json["data"]["buildTotalCash"])
            self.assertEqual(None, res.json["data"]["reduceInstNum"])
            self.assertEqual(None, res.json["data"]["reduceTotalCash"])
            self.assertEqual(None, res.json["data"]["cleanInstNum"])
            self.assertEqual(None, res.json["data"]["cleanTotalCash"])

    def test_it_should_200_when_symbol_is_exists(self):
        """Symbol 存在，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/chip-basic-info/DUMMY')
            self.assertEqual(200, res.status_code)
            self.assertEqual(10, res.json["data"]["cashSurplus"])
            self.assertEqual(10, res.json["data"]["cashNetIn"])
            self.assertEqual(20, res.json["data"]["cashNetOut"])
            self.assertEqual(10, res.json["data"]["addInstNum"])
            self.assertEqual(10, res.json["data"]["addTotalCash"])
            self.assertEqual(10, res.json["data"]["buildInstNum"])
            self.assertEqual(10, res.json["data"]["buildTotalCash"])
            self.assertEqual(10, res.json["data"]["reduceInstNum"])
            self.assertEqual(10, res.json["data"]["reduceTotalCash"])
            self.assertEqual(10, res.json["data"]["cleanInstNum"])
            self.assertEqual(10, res.json["data"]["cleanTotalCash"])
