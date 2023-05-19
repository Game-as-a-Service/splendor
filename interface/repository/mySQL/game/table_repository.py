from typing import Optional

from flask import session
from sqlalchemy.orm import Session,joinedload

from dbmodels.game_profile import TableInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation
from domain import Table




class TableRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get_player_node_info_by_id(self, game_id: str)->Table:
        table_info =(self._user_sql_session
                    .query(TableInfo)
                    .filter(TableInfo.game_id == game_id)
                    .first())

        return [Noble(noble.noble_id, noble.score, Bonus(noble.diamond, noble.sapphire, noble.emerald, noble.ruby, noble.onyx)) for noble in noble_infos]
