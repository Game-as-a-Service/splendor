from datetime import datetime
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy import or_
from sqlalchemy.orm import Query, Session

from api.common.datetime_utils import datetime_to_str
from dbmodels.nike.indicator_result import IndicatorResult


class IndicatorResultService:
    def __init__(self, nike_sql_session: Session) -> None:
        self._nike_sql_session = nike_sql_session

    def get_indicator_result(
            self,
            symbol: str,
            indicator: list,
            nums: int = None,
            start_at: Optional[str] = datetime_to_str(datetime.now() - relativedelta(years=15)),  # noqa: B008
            end_at: Optional[str] = datetime_to_str(datetime.now()),  # noqa: B008
    ) -> List[IndicatorResult]:
        query: Query = self._nike_sql_session.query(IndicatorResult) \
            .filter(IndicatorResult.symbol == symbol)

        if "monthly_avg_price" not in indicator:
            query = query.filter(IndicatorResult.indicator.in_(indicator))
        else:
            query = query.filter(or_(IndicatorResult.indicator.like('PE_stream%'),
                                     IndicatorResult.indicator.like('monthly%')))

        if start_at and end_at:
            query = query.filter(IndicatorResult.date.between(start_at, end_at))

        if nums:
            return query.order_by(IndicatorResult.date.desc()).limit(nums).all()

        return query.all()
