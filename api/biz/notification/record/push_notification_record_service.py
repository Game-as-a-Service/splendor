from datetime import datetime, timedelta
from logging import Logger
from typing import Tuple, List

from sqlalchemy import text
from sqlalchemy.orm import Session, Query

from api.biz.error import DataNotFound
from api.biz.notification.record import SORTED_BY, SORTED_WAY
from api.common.datetime_utils import date_to_str
from dbmodels.push_notification.push_notification_record import PushNotificationRecord


class PushNotificationRecordService:
    def __init__(
            self,
            logger: Logger,
            notice_sql_session: Session
    ):
        self._logger = logger
        self._notice_sql_session = notice_sql_session

    @staticmethod
    def orm_object_to_list(results: List[PushNotificationRecord]) -> List[dict]:
        data = []
        for r in results:
            data.append({
                "id": r.id,
                "createdAt": date_to_str(r.created_at),
                "strategyName": r.strategy_name,
                "strategyCategory": r.strategy_category,
                "settingType": r.setting_type,
                "readStatus": r.read_status,
                "advancedSettings": r.details,
                "notificationMethod": r.notification_method,
                "symbols": r.symbols
            })
        return data

    def get_push_notification_record_by_token_user_id(
            self,
            user_id: str,
            page: int,
            page_size: int,
            sort_by: str,
    ) -> Tuple[int, List[dict]]:
        _sort_by = SORTED_BY[sort_by[:-1]]
        # desc or asc
        _sort_way = SORTED_WAY[sort_by[-1]]
        # order by need to be improved
        query: Query = self._notice_sql_session \
            .query(PushNotificationRecord) \
            .filter(PushNotificationRecord.user_id == user_id,
                    PushNotificationRecord.created_at > (datetime.now() - timedelta(days=180))) \
            .order_by(text(f'{_sort_by} {_sort_way}, created_at desc'))

        # get all
        if page == -1 and page_size == -1:
            return query.count(), query.all()
        # get by page
        offset = (page - 1) * page_size
        return query.count(), self.orm_object_to_list(query.offset(offset).limit(page_size).all())

    def update_push_notification_record_by_user_id(
            self,
            user_id: str,
            id: int | None,
            payload: dict
    ) -> None:
        query: Query = self._notice_sql_session \
            .query(PushNotificationRecord) \
            .filter(PushNotificationRecord.user_id == user_id,
                    PushNotificationRecord.created_at > (datetime.now() - timedelta(days=180)))
        # update one record
        if id:
            query = query.filter(PushNotificationRecord.id == id)
            if query.one_or_none() is None:
                raise DataNotFound("Data not found")
        query.update({"read_status": payload["readStatus"]})

    def is_exist_record_unread(self, user_id: str) -> bool:
        res: List[PushNotificationRecord] = self._notice_sql_session \
            .query(PushNotificationRecord) \
            .filter(PushNotificationRecord.user_id == user_id,
                    PushNotificationRecord.created_at > (datetime.now() - timedelta(days=180)),
                    PushNotificationRecord.read_status == 0) \
            .first()

        if res is None:
            return False

        return True
