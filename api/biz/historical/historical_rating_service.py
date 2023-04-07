from datetime import datetime
from typing import List

import pandas as pd
from dateutil.relativedelta import relativedelta
from flask_caching import Cache
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

from api.biz.error import InvalidInvocation
from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import date_to_str


class HistoricalRatingService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session,
            symbol_service: SymbolService,
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session
        self._symbol_service = symbol_service

    def get_historical_rating_by_symbol_and_oriented(self, symbol: str, oriented: str) -> List[dict]:
        if oriented in ["value", "chip"]:
            symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)
        result: Result = self._nike_sql_session.execute(
            f"""
                SELECT * FROM historical_rating_{oriented} WHERE symbol='{symbol}'
                and version=(SELECT max(version) FROM historical_rating_{oriented} WHERE symbol='{symbol}')
                ORDER BY date ASC;
            """)
        return result.mappings().all()

    def historical_rating(self, symbol: str, oriented: str) -> dict:
        start_at = datetime(2007, 1, 1)
        end_at = datetime.today() - relativedelta(days=1)

        if oriented in ['value', 'chip']:
            result = self._concat_data(symbol, oriented, date_to_str(start_at), date_to_str(end_at))
            result = result.groupby(pd.Grouper(freq='W-FRI')).last().fillna(method='pad')[:end_at].dropna()
        elif oriented in ['trend', 'swing']:
            result = self._concat_data(symbol, oriented, date_to_str(start_at), date_to_str(end_at))
            result = result[:end_at].dropna()
        else:
            raise InvalidInvocation(f"{oriented} 不在可搜尋範圍內")

        result['date'] = result.index.strftime('%Y-%m-%d')
        result['rating'] = result['rating'].astype("int")
        return result.to_dict(orient='records')

    def _concat_data(self, symbol: str, oriented: str, start_at: str, end_at: str) -> pd.DataFrame:
        rating = self.get_historical_rating_by_symbol_and_oriented(symbol, oriented)
        price = self._symbol_service.get_symbol_price(symbol, start_at, end_at)

        symbol_rating = pd.DataFrame(rating).sort_values(
            ['date', 'created_at', 'updated_at'],
            ascending=[True, False, False]).drop_duplicates(
            subset=['date'], keep='first').set_index("date", drop=True)["value"].astype(int)
        symbol_rating.index = pd.to_datetime(symbol_rating.index).tolist()
        if oriented == 'chip':
            symbol_rating.index = symbol_rating.index.map(lambda date: date + relativedelta(days=45))

        symbol_price = pd.DataFrame(price).set_index("time", drop=True)["adj_close_price"].astype(float)
        symbol_price.index = pd.to_datetime(symbol_price.index).tolist()

        result = pd.concat({"rating": symbol_rating, "price": symbol_price}, axis=1, sort=True)
        return result
