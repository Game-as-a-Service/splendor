from datetime import datetime

from dateutil.relativedelta import relativedelta
from werkzeug.test import TestResponse

from dbmodels.nike.chip_institution_holding_info import ChipInstitutionHoldingInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiChipInstitutionHoldingInfo(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        for i in range(20):
            self.nike_sql_session.add(ChipInstitutionHoldingInfo(**{
                "symbol": "DUMMY",
                "date": datetime.now() - relativedelta(months=i * 3),
                "inst_ownshp": 120.12,
                "inst_count": 50
            }))
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(ChipInstitutionHoldingInfo).filter(
            ChipInstitutionHoldingInfo.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/chip-institution-holding/DUMMY')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_symbol_not_found(self):
        """找不到Symbol，但會回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/chip-institution-holding-info/SAMPLE')
            self.assertEqual(200, res.status_code)
            self.assertIsNone(res.json["data"]["headYear"])
            self.assertIsNone(res.json["data"]["tailYear"])
            self.assertEqual([], res.json["data"]["infos"])

    def test_it_should_200_when_symbol_is_exists(self):
        """Symbol 存在，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/chip-institution-holding-info/DUMMY')
            self.assertEqual(200, res.status_code)
            self.assertEqual(2018, res.json["data"]["headYear"])
            self.assertEqual(2023, res.json["data"]["tailYear"])
            self.assertEqual(20, len(res.json["data"]["infos"]))
