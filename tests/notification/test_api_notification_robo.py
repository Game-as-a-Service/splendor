from werkzeug.test import TestResponse

from api.common.datetime_utils import date_to_str
from dbmodels.push_notification.push_notification_robo import PushNotificationRobo
from tests import setup_basic_session, setup_free_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiNotificationRobo(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.notice_sql_session.add_all([
            PushNotificationRobo(**{
                "user_id": "basic-user",
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
            }),
            PushNotificationRobo(**{
                "user_id": "basic-user",
                "strategy_name": "dummy-2",
                "strategy_category": "sell",
                "notification_method": "line",
                "finished_at": "2023-02-05",
                "status": "inactive",
                "symbols": ["AAPL"],
                "setting_type": "custom",
                "details": {
                    "value": {"variation": "crossing-up", "score": 2},
                    "squeezeDaily": {"action": "energy-fire", "squeeze": "up"},
                }
            })
        ])
        self.notice_sql_session.flush()

    def _clear_test_data(self):
        self.notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.strategy_name.in_(["dummy-1", "dummy-2", "dummy-3", "dummy-4", "dummy-5",
                                                            "modify-dummy"])) \
            .delete()
        self.notice_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/notification/robo/value')
            self.assertEqual(404, res.status_code)

            res: TestResponse = client.post('/notification/robs')
            self.assertEqual(404, res.status_code)

            res: TestResponse = client.put('/notification/robo/value')
            self.assertEqual(404, res.status_code)

    def test_it_should_404_when_not_found_robo(self):
        """沒有找到指定的 id 推播機器人，應該回應 404"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.get('/notification/robo/10000')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_free_member_get_robo_setting(self):
        """[免費用戶] 抓取推播機器人資訊，應該回應 200"""
        with self.app.test_client() as client:
            setup_free_session(client)

            res: TestResponse = client.get("/notification/robo")
            self.assertEqual(200, res.status_code)
            self.assertEqual(0, len(res.json["data"]))

    def test_it_should_200_when_sub_member_get_robo_setting(self):
        """[訂閱用戶] 抓取推播機器人資訊，應該回應 200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            raw: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "basic-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            res: TestResponse = client.get(f'/notification/robo/{raw.id}')
            self.assertEqual(200, res.status_code)
            data = res.json["data"]
            self.assertEqual("dummy-1", data["strategyName"])
            self.assertEqual("buy", data["strategyCategory"])
            self.assertEqual("email", data["notificationMethod"])
            self.assertEqual("2023-01-31", data["finishedAt"])
            self.assertEqual("active", data["status"])
            self.assertListEqual(["AAPL"], data["symbols"])
            self.assertEqual("custom", data["settingType"])
            self.assertDictEqual({
                "chip": {"variation": "crossing-up", "score": 1},
                "surfingTrendWeekly": "neg2pos",
            }, data["advancedSettings"])

            res: TestResponse = client.get("/notification/robo")
            self.assertEqual(200, res.status_code)
            self.assertEqual(2, len(res.json["data"]))

    def test_it_should_200_when_free_number_create_robo(self):
        """[免費用戶] 建立推播機器人，應該回應 200"""
        with self.app.test_client() as client:
            setup_free_session(client)
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "chip": {"variation": "crossing-up", "score": 1},
                    "surfingTrendWeekly": "moving-up",
                    "squeezeDaily": {"action": "energy-fire", "squeeze": "up"},
                    "marketCap": "medium-stock",
                    "greaterThanVolume20MA": 1
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(200, res.status_code)

            raw: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "free-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-3") \
                .first()

            self.assertEqual("dummy-3", raw.strategy_name)
            self.assertEqual("buy", raw.strategy_category)
            self.assertEqual("email", raw.notification_method)
            self.assertEqual("2023-02-01", date_to_str(raw.finished_at))
            self.assertListEqual(["TSLA"], raw.symbols)
            self.assertEqual("custom", raw.setting_type)
            self.assertDictEqual({
                "chip": {"variation": "crossing-up", "score": 1},
                "surfingTrendWeekly": "moving-up",
                "squeezeDaily": {"action": "energy-fire", "squeeze": "up"},
                "marketCap": "medium-stock",
                "greaterThanVolume20MA": 1
            }, raw.details)

            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(429, res.status_code)

    def test_it_should_200_when_sub_number_create_robo(self):
        """[訂閱用戶] 建立推播機器人，應該回應 200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            payload = {
                "strategyName": "dummy-4",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "chip": {"variation": "crossing-up", "score": 1},
                    "surfingTrendWeekly": "moving-up",
                    "squeezeDaily": {"action": "energy-fire", "squeeze": "up"},
                    "marketCap": "medium-stock",
                    "greaterThanVolume20MA": 1
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(200, res.status_code)

            raw: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "basic-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-4") \
                .first()

            self.assertEqual("dummy-4", raw.strategy_name)
            self.assertEqual("buy", raw.strategy_category)
            self.assertEqual("email", raw.notification_method)
            self.assertEqual("2023-02-01", date_to_str(raw.finished_at))
            self.assertListEqual(["TSLA"], raw.symbols)
            self.assertEqual("custom", raw.setting_type)
            self.assertDictEqual({
                "chip": {"variation": "crossing-up", "score": 1},
                "surfingTrendWeekly": "moving-up",
                "squeezeDaily": {"action": "energy-fire", "squeeze": "up"},
                "marketCap": "medium-stock",
                "greaterThanVolume20MA": 1
            }, raw.details)

            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(200, res.status_code)

            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(429, res.status_code)

    def test_it_should_200_when_modify_robo_settings(self):
        """修改推播機器人設定，應該回應 200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            before_raw: PushNotificationRobo = self.notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.user_id == "basic-user") \
                .filter(PushNotificationRobo.strategy_name == "dummy-1") \
                .first()

            payload = {
                "strategyName": "modify-dummy",
                "strategyCategory": "sell",
                "notificationMethod": "line",
                "finishedAt": "2023-03-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "dividend": {"variation": "crossing-up", "score": 5},
                }
            }
            res: TestResponse = client.put(f"/notification/robo/{before_raw.id}", json=payload)
            self.assertEqual(res.status_code, 200)

    def test_it_should_422_when_payload_key_invalid(self):
        """Payload Key 有誤，應該回應 422"""
        with self.app.test_client() as client:
            setup_free_session(client)

            # payload strategyName 名稱錯誤
            payload = {
                "strategyaName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload strategyCategory 名稱錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyaCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload notificationMethod 名稱錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethoda": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload finishedAt 名稱錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedaAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload symbols 名稱錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbolsa": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload settingType 名稱錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingTypea": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload advancedSettings 名稱錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettingsa": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload strategyName 型態錯誤
            payload = {
                "strategyName": 1,
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload strategyCategory 型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": 1,
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload notificationMethod 型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": 1,
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload finishedAt 型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": 1,
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload symbols 型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": 1,
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload settingType 型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": 1,
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

            # payload advancedSettings 型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": 1
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(422, res.status_code)

    def test_it_should_400_when_payload_value_invalid(self):
        """Payload Value 有誤，應該回應 400"""
        with self.app.test_client() as client:
            setup_free_session(client)

            # payload strategyCategory 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "test",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(400, res.status_code)

            # payload notificationMethod 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "test",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(400, res.status_code)

            # payload finishedAt 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "test",
                "finishedAt": "2023-02-00",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(400, res.status_code)

            # payload settingType 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "test",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "test",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "test",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {}
            }
            res: TestResponse = client.post('/notification/robo', json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "123": 123,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "123": 123,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "123": 123,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - oriented 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "value": "",
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - oriented 只有 variation 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "value": {"variation": ""},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - oriented 只有 score 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "value": {"score": ""},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - surfingTrendDaily 資料型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "surfingTrendDaily": 1,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - surfingTrendDaily 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "surfingTrendDaily": "123",
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - surfingTrendWeekly 資料型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "surfingTrendWeekly": 1,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - surfingTrendWeekly 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "surfingTrendWeekly": "123",
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - squeezeDaily 資料型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": 1,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - squeezeDaily action 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": {"action": "123", "squeeze": "up"},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - squeezeDaily squeeze 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": {"action": "energy-accumulate", "squeeze": "1"},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - squeezeDaily 資料錯誤，選擇 當下狀態 energy-accumulate 時，energy 必須要選
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": {"action": "energy-accumulate", "squeeze": "up"},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - squeezeDaily energy 資料錯誤， 必須要為陣列且只能有 0 -3 的數字
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": {"action": "energy-accumulate", "squeeze": "up", "energy": 0},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": {"action": "energy-accumulate", "squeeze": "up", "energy": ["123"]},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - squeezeDaily 資料錯誤，選擇 動能發動 energy-fire 時，不能有 energy
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "squeezeDaily": {"action": "energy-fire", "squeeze": "up", "energy": 0},
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - marketCap 資料型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "marketCap": 1,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - marketCap 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "marketCap": "123",
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - greaterThanVolume20MA 資料型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "greaterThanVolume20MA": "0.2",
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - greaterThanVolume20MA 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "greaterThanVolume20MA": 0.3,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - lessThanVolume20MA 資料型態錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "lessThanVolume20MA": "0.2",
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)

            # payload advancedSettings - lessThanVolume20MA 資料錯誤
            payload = {
                "strategyName": "dummy-3",
                "strategyCategory": "buy",
                "notificationMethod": "email",
                "finishedAt": "2023-02-01",
                "symbols": ["TSLA"],
                "settingType": "custom",
                "advancedSettings": {
                    "lessThanVolume20MA": 0.3,
                }
            }
            res: TestResponse = client.post("/notification/robo", json=payload)
            self.assertEqual(400, res.status_code)
