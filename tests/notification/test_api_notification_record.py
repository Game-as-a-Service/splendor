from random import choice

from werkzeug.test import TestResponse

from dbmodels.push_notification.push_notification_record import PushNotificationRecord
from tests import setup_guest_session, setup_basic_session, setup_free_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiNotificationRecord(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.notice_sql_session.add(PushNotificationRecord(**{
            "id": '1',
            "user_id": 'free-user',
            "strategy_name": choice(["策略1", "策略2", "策略3", "策略4", "策略5"]),
            "strategy_category": choice(["SELL", "BUY"]),
            "setting_type": choice(["self-robo", "value-robo", "swing-robo", "trend-robo"]),
            "notification_method": choice(["EMAIL", "LINE"]),
            "symbols": "DUMMY",
            "details": "test",
            "read_status": choice([True, False])
        }))
        for _i in range(15):
            self.notice_sql_session.add(PushNotificationRecord(**{
                "id": str(_i + 2),
                "user_id": choice(['free-user', 'basic-user', 'business-user']),
                "strategy_name": choice(["策略1", "策略2", "策略3", "策略4", "策略5"]),
                "strategy_category": choice(["SELL", "BUY"]),
                "setting_type": choice(["self-robo", "value-robo", "swing-robo", "trend-robo"]),
                "notification_method": choice(["EMAIL", "LINE"]),
                "symbols": "DUMMY",
                "details": "test",
                "read_status": choice([True, False])
            }))
            self.notice_sql_session.flush()

    def _clear_test_data(self):
        self.notice_sql_session.query(PushNotificationRecord).filter(PushNotificationRecord.symbols == "DUMMY").delete()
        self.notice_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/wrong-url')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_all_good(self):
        """success 回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/notification/record/1/10?sortBy=settingType1")
            self.assertEqual(200, res.status_code)

    def test_it_should_400_when_parameter_invalid(self):
        """In query Parameter 參數錯誤，應該回應400"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/notification/record/1/10?sortBy=wrongParameter=1")
            self.assertEqual(400, res.status_code)

    def test_it_should_409_when_guest_and_symbol_exists_and_page_1(self):
        """[Guest] 不允許查詢，應該權限不足回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/notification/record/1/10?sortBy=settingType1",
                                           headers={"x-api-key": "Guest"})
            self.assertEqual(409, res.status_code)

    def test_it_should_200_when_free_plan_and_symbol_exists_and_page_1(self):
        """[免費方案] 取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.get("/notification/record/1/10?sortBy=settingType1")
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_basic_plan_and_symbol_exists_and_page_1(self):
        """[基礎方案] 取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/notification/record/1/10?sortBy=settingType1")
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_basic_plan_and_symbol_exists_and_page_2(self):
        """[基礎方案] 取第二頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get("/notification/record/6/10?sortBy=settingType1")
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_business_plan_and_symbol_exists_and_page_1(self):
        """[企業方案] 取第一頁資訊，應該回應200"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/notification/record/1/10?sortBy=settingType1")
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_update_all_logs(self):
        """success 回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            payload = {
                "readStatus": 0
            }
            res: TestResponse = client.put("/notification/record", json=payload)
            self.assertEqual(200, res.status_code)
            _data = self.notice_sql_session.query(PushNotificationRecord).filter(
                PushNotificationRecord.user_id == 'free-user',
                PushNotificationRecord.read_status == 1).one_or_none()
            self.assertEqual(_data, None)

    def test_it_should_200_when_update_one_log(self):
        """success 回應200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            payload = {
                "readStatus": 1
            }
            res: TestResponse = client.put("/notification/record/1", json=payload)
            self.assertEqual(200, res.status_code)
            _data = self.notice_sql_session.query(PushNotificationRecord).filter(
                PushNotificationRecord.id == 'free-user',
                PushNotificationRecord.read_status == 0).one_or_none()
            self.assertEqual(_data, None)

    def test_it_should_404_when_data_not_found(self):
        """data_not_found，應該回應404"""
        with self.app.test_client() as client:
            setup_free_session(client)
            payload = {
                "readStatus": 1
            }
            res: TestResponse = client.put("/notification/record/999", json=payload)
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_lack_of_payload(self):
        """lack of payload，應該回應400"""
        with self.app.test_client() as client:
            setup_free_session(client)
            res: TestResponse = client.put("/notification/record/1")
            self.assertEqual(400, res.status_code)

    def test_it_should_400_when_payload_data_not_permitted(self):
        """readStatus not permitted，應該回應400"""
        with self.app.test_client() as client:
            setup_free_session(client)
            payload = {
                "readStatus": 4
            }
            res: TestResponse = client.put("/notification/record/1", json=payload)
            self.assertEqual(400, res.status_code)
