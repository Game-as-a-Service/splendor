from werkzeug.test import TestResponse

from dbmodels.push_notification.push_notification_robo import PushNotificationRobo
from tests import setup_free_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiNotificationRoboStatus(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.notice_sql_session.add(
            PushNotificationRobo(**{
                "user_id": "free-user",
                "strategy_name": "dummy-1",
                "strategy_category": "buy",
                "notification_method": "email",
                "finished_at": "2023-01-31",
                "status": "active",
                "symbols": ["AAPL"],
                "setting_type": "custom",
                "details": {
                    "chip": {"variation": "crossing-up", "score": 1},
                    "surfingTrendWeekly": "neg2pos",
                }
            })
        )
        self.notice_sql_session.flush()

    def _clear_test_data(self):
        self.notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.strategy_name.in_(["dummy-1"])) \
            .delete()
        self.notice_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/notification/robo-status/value')
            self.assertEqual(404, res.status_code)

            res: TestResponse = client.post('/notification/robo-status/value')
            self.assertEqual(404, res.status_code)

            res: TestResponse = client.put('/notification/robo-status')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_status_to_inactive(self):
        """URL 和 Payload 正確，status 變更為 inactive"""
        with self.app.test_client() as client:
            setup_free_session(client)

            robo: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "free-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            res: TestResponse = client.post(f'/notification/robo-status/{robo.id}', json={"status": "inactive"})
            self.assertEqual(200, res.status_code)

    def test_it_should_200_when_status_to_deleted(self):
        """URL 和 Payload 正確，status 變更為 deleted"""
        with self.app.test_client() as client:
            setup_free_session(client)

            robo: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "free-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            res: TestResponse = client.post(f'/notification/robo-status/{robo.id}', json={"status": "deleted"})
            self.assertEqual(200, res.status_code)

    def test_it_should_429_when_active_limit_reached(self):
        """已達可運行的策略機器人上限，應該回應 429"""
        with self.app.test_client() as client:
            setup_free_session(client)

            robo: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "free-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            res: TestResponse = client.post(f'/notification/robo-status/{robo.id}',
                                            json={"status": "active", "finishedAt": "2023-02-03"})
            self.assertEqual(429, res.status_code)

    def test_it_should_422_when_payload_key_invalid(self):
        """Payload Key 有誤，應該回應 422"""
        with self.app.test_client() as client:
            setup_free_session(client)

            robo: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "free-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            res: TestResponse = client.post(f'/notification/robo-status/{robo.id}',
                                            json={"abc": "active"})
            self.assertEqual(422, res.status_code)

    def test_it_should_400_when_payload_value_invalid(self):
        """Payload value 有誤，應該回應 400"""
        with self.app.test_client() as client:
            setup_free_session(client)

            robo: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "free-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            res: TestResponse = client.post(f'/notification/robo-status/{robo.id}',
                                            json={"status": "abc"})
            self.assertEqual(400, res.status_code)
