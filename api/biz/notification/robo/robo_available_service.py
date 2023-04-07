from flask import session
from sqlalchemy.orm import Session

from api.biz.error import guard_valid_data, guard_valid_param, InvalidInvocation, RateLimitingExceededError
from api.biz.notification.robo import REQUIRED, OPTIONAL, STRATEGY_CATEGORY, NOTIFICATION_METHODS, SETTING_TYPE, \
    VARIATION, SCORE, SURFING_TREND, MARKET_CAP, SQUEEZE_ACTION, SQUEEZE, \
    SQUEEZE_ENERGY
from api.common.datetime_utils import str_to_date
from dbmodels.push_notification.push_notification_robo import PushNotificationRobo


class RoboAvailableService:
    def __init__(self, notice_sql_session: Session):
        self._notice_sql_session = notice_sql_session

    def get_notification_robo(self, id: int) -> PushNotificationRobo:
        return self._notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.id == id) \
            .filter(PushNotificationRobo.user_id == session["user_id"]) \
            .first()

    def available_create(self, payload: dict) -> None:
        self._check_robo_counts()
        self._basic_check(payload)

    def available_modify_settings(self, id: int, payload: dict) -> None:
        robo = self.get_notification_robo(id)
        if not robo:
            raise InvalidInvocation(f"未找到 id ({id}) 的推播機器人")

        self._basic_check(payload)

    def available_modify_status(self, id: int, payload: dict) -> None:
        robo = self.get_notification_robo(id)
        if not robo:
            raise InvalidInvocation(f"未找到 id ({id}) 的推播機器人")

        guard_valid_data(payload.get("status"), "payload 應要有 status")
        guard_valid_param(payload["status"] in ["active", "inactive", "deleted"],
                          "status 應為 active、inactive、deleted")
        if payload["status"] == "active":
            self._check_robo_counts()
            guard_valid_data(payload.get("finishedAt"), "status 為 active，應該要有 finishedAt")
            guard_valid_param(str_to_date(payload["finishedAt"]), "finishedAt 格式應為 %Y-%m-%d")

    def _check_robo_counts(self) -> None:
        counts = self._notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.user_id == session["user_id"]) \
            .filter(PushNotificationRobo.status == "active") \
            .count()

        if session["plan"] == "Free" and counts == 1:
            raise RateLimitingExceededError("目前運行中的機器人已達上限")

        if session["plan"] in ["Basic Monthly", "Basic Yearly"] and counts == 3:
            raise RateLimitingExceededError("目前運行中的機器人已達上限")

    def _basic_check(self, payload: dict):
        self._payload_required(payload)
        self._check_required_type(payload)
        self._check_required_value(payload)

        self._check_optional_key(payload["advancedSettings"])
        self._check_optional_value(payload["advancedSettings"])

    @staticmethod
    def _payload_required(payload):
        for p in REQUIRED:
            guard_valid_data(p in payload, f"缺少 {p} 參數")

    @staticmethod
    def _check_required_type(payload):
        guard_valid_data(isinstance(payload["strategyName"], str), "strategyName 必須為字串")
        guard_valid_data(isinstance(payload["strategyCategory"], str), "strategyCategory 必須為字串")
        guard_valid_data(isinstance(payload["notificationMethod"], str), "notificationMethod 必須為字串")
        guard_valid_data(isinstance(payload["finishedAt"], str), "finishedAt 必須為字串")
        guard_valid_data(isinstance(payload["symbols"], list), "symbols 必須為陣列")
        guard_valid_data(isinstance(payload["settingType"], str), "settingType 必須為字串")
        guard_valid_data(isinstance(payload["advancedSettings"], dict), "advancedSettings 必須為 JSON")

    @staticmethod
    def _check_required_value(payload):
        guard_valid_param(payload["strategyCategory"] in STRATEGY_CATEGORY, "strategyCategory 應為 buy 或 sell")
        guard_valid_param(str_to_date(payload["finishedAt"]), "finishedAt 格式應為 %Y-%m-%d")
        guard_valid_param(payload["notificationMethod"] in NOTIFICATION_METHODS,
                          "notificationMethod 應為 email 或 line")
        guard_valid_param(
            payload["settingType"] in SETTING_TYPE, "settingType 應為 custom、value-robo、swing-robo、trend-robo")
        guard_valid_param(payload["advancedSettings"] != {}, "advancedSettings 至少需填一組設定")

    @staticmethod
    def _check_optional_key(payload):
        for p in payload:
            guard_valid_param(p in OPTIONAL, f"{p} 不在進階設定範圍內")

    @staticmethod
    def _check_optional_value(payload):
        for key in payload:
            if key in ["value", "trend", "swing", "chip", "dividend"]:
                guard_valid_param(isinstance(payload[key], dict), f"{key} 必須為 JSON")
                guard_valid_param("variation" in payload[key], f"{key} 應要有 variation 參數")
                guard_valid_param("score" in payload[key], f"{key} 應要有 score 參數")
                guard_valid_param(payload[key]["variation"] in VARIATION,
                                  f"{key} 應為 crossing-up、crossing-down、greater-than-equal 或 less-than-equal")
                guard_valid_param(payload[key]["score"] in SCORE, f"{key} 應為 1、2、3、4 或 5")

            elif key in ["surfingTrendDaily", "surfingTrendWeekly"]:
                guard_valid_param(isinstance(payload[key], str), f"{key} 必須為字串")
                guard_valid_param(payload[key] in SURFING_TREND,
                                  f"{key} 應為 neg2pos、pos2neg、moving-up 或 moving-down")

            elif key in ["squeezeDaily", "squeezeWeekly"]:
                guard_valid_param(isinstance(payload[key], dict), f"{key} 必須為 JSON")
                guard_valid_param(payload[key]["action"] in SQUEEZE_ACTION,
                                  "action 必須為 energy-accumulate 或 energy-fire")
                guard_valid_param(payload[key]["squeeze"] in SQUEEZE, "squeeze 必須為 any、up 或 down")

                if payload[key]["action"] == "energy-accumulate":
                    guard_valid_param("energy" in payload[key], "action 選擇 energy-accumulation 時，energy 必須要選")
                    guard_valid_param(isinstance(payload[key]["energy"], list), f"{key} 必須為陣列")
                    guard_valid_param(all(item in SQUEEZE_ENERGY for item in payload[key]["energy"]),
                                      "energy 陣列內的資料必須為 0-3 之間的整數")
                else:
                    guard_valid_param("energy" not in payload[key],
                                      "energy 只有在選擇 能量累積時 energy-accumulation 時才能選擇")

            elif key in ["marketCap"]:
                guard_valid_param(isinstance(payload[key], str), f"{key} 必須為字串")
                guard_valid_param(payload[key] in MARKET_CAP,
                                  f"{key} 應為 micro-stock、small-stock、medium-stock 或 large-stock")

            elif key in ["greaterThanVolume20MA", "lessThanVolume20MA"]:
                guard_valid_param(isinstance(payload[key], int), f"{key} 必須為整數")
                guard_valid_param(1 <= payload[key] <= 100, f"{key} 應為 1-100")

            else:
                raise InvalidInvocation(f"{key} 不在進階設定範圍內")
