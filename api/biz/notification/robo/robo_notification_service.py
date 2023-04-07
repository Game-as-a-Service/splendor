from logging import Logger
from typing import Optional, List, Union

from flask import session
from sqlalchemy.orm import Session

from api.biz.error import DataNotFound
from api.biz.notification.robo.robo_available_service import RoboAvailableService
from api.common.datetime_utils import date_to_str
from dbmodels.push_notification.push_notification_robo import PushNotificationRobo


class RoboNotificationService:
    def __init__(
            self,
            logger: Logger,
            notice_sql_session: Session,
            robo_available_service: RoboAvailableService
    ):
        self._logger = logger
        self._notice_sql_session = notice_sql_session
        self._robo_available_service = robo_available_service

    def get_notification_robo_by_id(self, id: int) -> PushNotificationRobo:
        return self._notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.id == id) \
            .first()

    def get_all_notification_robo(self) -> List[PushNotificationRobo]:
        return self._notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.user_id == session["user_id"]) \
            .filter(PushNotificationRobo.status.in_(["active", "inactive"])) \
            .order_by(PushNotificationRobo.finished_at.desc()) \
            .all()

    def update_notification_robo(self, id: int, data: dict):
        self._notice_sql_session.query(PushNotificationRobo) \
            .filter(PushNotificationRobo.id == id) \
            .filter(PushNotificationRobo.user_id == session["user_id"]) \
            .update(data)

    def create_notification(self, payload: dict) -> None:
        self._robo_available_service.available_create(payload)

        self._notice_sql_session.add(PushNotificationRobo(**{
            "user_id": session["user_id"],
            "strategy_name": payload["strategyName"],
            "strategy_category": payload["strategyCategory"],
            "status": "active",
            "setting_type": payload["settingType"],
            "notification_method": payload["notificationMethod"],
            "symbols": payload["symbols"],
            "details": payload["advancedSettings"],
            "finished_at": payload["finishedAt"]
        }))
        self._notice_sql_session.flush()

    def modify_notification_settings(self, id: int, payload: dict) -> None:
        self._robo_available_service.available_modify_settings(id, payload)
        data = {
            "user_id": session["user_id"],
            "strategy_name": payload["strategyName"],
            "strategy_category": payload["strategyCategory"],
            "setting_type": payload["settingType"],
            "notification_method": payload["notificationMethod"],
            "symbols": payload["symbols"],
            "details": payload["advancedSettings"],
            "finished_at": payload["finishedAt"]
        }
        self.update_notification_robo(id, data)

    def modify_notification_status(self, id: int, payload: dict) -> None:
        self._robo_available_service.available_modify_status(id, payload)
        if payload["status"] == "active":
            self.update_notification_robo(id, {"status": payload["status"], "finished_at": payload["finishedAt"]})
            return
        self.update_notification_robo(id, payload)

    def get_notification_robo(self, id: Optional[int] = None) -> Union[dict, List[dict]]:
        if id:
            raw: PushNotificationRobo = self._notice_sql_session.query(PushNotificationRobo) \
                .filter(PushNotificationRobo.id == id) \
                .filter(PushNotificationRobo.user_id == session["user_id"]) \
                .first()

            if not raw:
                raise DataNotFound(f"未找到 id ({id}) 的推播機器人")

            return {
                "id": raw.id,
                "strategyName": raw.strategy_name,
                "strategyCategory": raw.strategy_category,
                "status": raw.status,
                "notificationMethod": raw.notification_method,
                "symbols": raw.symbols,
                "finishedAt": date_to_str(raw.finished_at),
                "settingType": raw.setting_type,
                "advancedSettings": raw.details
            }

        raws: List[PushNotificationRobo] = self.get_all_notification_robo()
        data = []

        for r in raws:
            data.append({
                "id": r.id,
                "strategyName": r.strategy_name,
                "strategyCategory": r.strategy_category,
                "status": r.status,
                "notificationMethod": r.notification_method,
                "symbols": r.symbols,
                "finishedAt": date_to_str(r.finished_at),
                "settingType": r.setting_type,
                "advancedSettings": r.details
            })

        return data
