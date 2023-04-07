from random import choice

from werkzeug.test import TestResponse

from dbmodels.push_notification.push_notification_record import PushNotificationRecord
from tests import setup_guest_session, setup_free_session, setup_business_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiNotificationRecordRead(BaseFlaskTestCase):

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
                "user_id": choice(['free-user', 'basic-user']),
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
            res: TestResponse = client.get("/notification/record/unread")
            self.assertEqual(200, res.status_code)

    def test_it_should_409_when_guest_and_symbol_exists_and_page_1(self):
        """[Guest] 不允許查詢，應該權限不足回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            res: TestResponse = client.get("/notification/record/unread",
                                           headers={"x-api-key": "Guest"})
            self.assertEqual(409, res.status_code)

    def test_it_should_200_when_no_data(self):
        """No data"""
        with self.app.test_client() as client:
            setup_business_session(client)
            res: TestResponse = client.get("/notification/record/unread")
            self.assertEqual(200, res.status_code)
            self.assertEqual(res.data, b'{"data": {"hasUnread": false}, "message": "Success"}')
