from datetime import datetime

from werkzeug.test import TestResponse

from dbmodels.nike.indicator_result import IndicatorResult
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiSymbolValueIndicator(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        for idx in [
            "REVENUE_YOY_MRQ", "REVENUE_YOY_MRT", "REVENUE_YOY_MRY",
            "NCFO_NETINC_ratio_MRQ", "NCFO_NETINC_ratio_MRT", "NCFO_NETINC_ratio_MRY",
            "EPS_MRQ", "EPS_MRT", "EPS_MRY",
            "ROE_MRQ", "ROE_MRT", "ROE_MRY",
            "ROA_MRQ", "ROA_MRT", "ROA_MRY",
            "ROS_MRQ", "ROS_MRT", "ROS_MRY",
            "ROIC_MRQ", "ROIC_MRT", "ROIC_MRY",
            "monthly_avg_price",
            "PE_stream_1_1.1", "PE_stream_2_2.2", "PE_stream_3_3.3",
            "PE_stream_4_4.4", "PE_stream_5_5.5", "PE_stream_6_6.6",
        ]:
            self.nike_sql_session.add_all([
                IndicatorResult(**{
                    "symbol": "DUMMY",
                    "date": "2022-07-07",
                    "indicator": idx,
                    "value": 1.1
                })
            ])
        self.nike_sql_session.flush()

    def _clear_test_data(self):
        self.nike_sql_session.query(IndicatorResult).filter(IndicatorResult.symbol == "DUMMY").delete()
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/')
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_indicator_not_in_map(self):
        """indicator不符合規定，應該回應400"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/DUMMY/ABC')
            self.assertEqual(400, res.status_code)

    def test_it_should_200_when_filter_revenue_yoy(self):
        """搜尋REVENUE-YOY因子，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/DUMMY/REVENUE-YOY')
            self.assertEqual(200, res.status_code)
            pre_data = {
                "REVENUE_YOY_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "REVENUE_YOY_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "REVENUE_YOY_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "updatedAt": datetime.now().strftime("%Y-%m-%d")
            }
            self.assertDictEqual(pre_data, res.json["data"])

    def test_it_should_200_when_filter_ncfo_netinc(self):
        """搜尋NCFO-NETINC因子，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/DUMMY/NCFO-NETINC')
            self.assertEqual(200, res.status_code)
            pre_data = {
                "NCFO_NETINC_ratio_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "NCFO_NETINC_ratio_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "NCFO_NETINC_ratio_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "updatedAt": datetime.now().strftime("%Y-%m-%d")
            }
            self.assertDictEqual(pre_data, res.json["data"])

    def test_it_should_200_when_filter_eps(self):
        """搜尋EPS因子，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/DUMMY/EPS')
            self.assertEqual(200, res.status_code)
            pre_data = {
                "EPS_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "EPS_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "EPS_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "updatedAt": datetime.now().strftime("%Y-%m-%d")
            }
            self.assertDictEqual(pre_data, res.json["data"])

    def test_it_should_200_when_filter_roe_roa_ros_roic(self):
        """搜尋ROE-ROA-ROS-ROIC因子，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/DUMMY/ROE-ROA-ROS-ROIC')
            self.assertEqual(200, res.status_code)
            pre_data = {
                "ROE_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "ROA_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "ROS_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "ROIC_MRQ": [{"date": "2022-07-07", "score": 1.1}],
                "ROE_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "ROA_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "ROS_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "ROIC_MRT": [{"date": "2022-07-07", "score": 1.1}],
                "ROE_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "ROA_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "ROS_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "ROIC_MRY": [{"date": "2022-07-07", "score": 1.1}],
                "updatedAt": datetime.now().strftime("%Y-%m-%d")
            }
            self.assertDictEqual(pre_data, res.json["data"])

    def test_it_should_200_when_filter_pe_ratio(self):
        """搜尋PE-RATIO因子，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/value-indicator/DUMMY/PE-RATIO')
            self.assertEqual(200, res.status_code)
            pre_data = {
                "monthlyAvgPrice": [{"date": "2022-07-07", "score": 1.1}],
                "PE_stream_1": {"text": "1.1倍本益比", "data": [{"date": "2022-07-07", "score": 1.1}], },
                "PE_stream_2": {"text": "2.2倍本益比", "data": [{"date": "2022-07-07", "score": 1.1}], },
                "PE_stream_3": {"text": "3.3倍本益比", "data": [{"date": "2022-07-07", "score": 1.1}], },
                "PE_stream_4": {"text": "4.4倍本益比", "data": [{"date": "2022-07-07", "score": 1.1}], },
                "PE_stream_5": {"text": "5.5倍本益比", "data": [{"date": "2022-07-07", "score": 1.1}], },
                "PE_stream_6": {"text": "6.6倍本益比", "data": [{"date": "2022-07-07", "score": 1.1}], },
                "updatedAt": datetime.now().strftime("%Y-%m-%d")
            }
            self.assertEqual(pre_data, res.json["data"])
