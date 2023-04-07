from typing import Optional

from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

from api.common.datetime_utils import date_to_str


class UpdatedAtUtils:
    def __init__(self, nike_sql_session: Session, sec13f_sql_session: Session):
        self._nike_sql_session = nike_sql_session
        self._sec13f_sql_session = sec13f_sql_session

    def get_date(self, db: str, table: str, fmt: str = "%Y-%m-%d") -> Optional[str]:
        if db == "nike":
            sql = f"SELECT max(updated_at) AS updated_at, max(created_at) AS created_at FROM {table};"
            result: CursorResult = self._nike_sql_session.execute(sql)

            for r in result:
                updated_at = date_to_str(r.updated_at, fmt)
                created_at = date_to_str(r.created_at, fmt)

            if updated_at:
                return max(updated_at, created_at)
            return created_at

        if db == "13F":
            sql = f"SELECT max(calendardate) AS calendardate FROM {table};"
            result: CursorResult = self._sec13f_sql_session.execute(sql)

            for r in result:
                updated_at = date_to_str(r.calendardate, fmt)

            if updated_at:
                return updated_at

            return None

        return None
