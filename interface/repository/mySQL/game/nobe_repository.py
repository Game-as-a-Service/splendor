from typing import Optional

from flask import session
from sqlalchemy.orm import Session,joinedload

from dbmodels.game_profile import PlayerNobleInfo,NobleInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation
from domain import Noble,Bonus
from typing import List
from application.user_case import NobleUserCase,BonusUserCase


class NobeRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    @staticmethod
    def get_player_node_info_by_id(self, game_id: str, player_id: str)->List[NobleUserCase]:
        noble_infos:List[NobleInfo] =(self._user_sql_session
                                        .query(NobleInfo)
                                        .join(PlayerNobleInfo, PlayerNobleInfo.noble_id == NobleInfo.noble_id)
                                        .filter(PlayerNobleInfo.game_id == game_id)
                                        .filter(PlayerNobleInfo.player_id == player_id)
                                        .all())

        return [NobleUserCase.to_usercase(noble.noble_id, noble.score, BonusUserCase.to_usercase(noble.diamond, noble.sapphire, noble.emerald, noble.ruby, noble.onyx)) for noble in noble_infos]

    @staticmethod
    def set_player_node_info_by_id(self, game_id: str, player_id: str,nobles:List[NobleUserCase])->None:
        nobles_origin: List[PlayerNobleInfo] =(self._user_sql_session
                                                .query(PlayerNobleInfo)
                                                .join(NobleInfo, PlayerNobleInfo.noble_id == NobleInfo.noble_id)
                                                .filter(PlayerNobleInfo.game_id == game_id)
                                                .filter(PlayerNobleInfo.player_id == player_id)
                                                .all())
        
        nobles_new =[PlayerNobleInfo.from_noble(noble,game_id,player_id) for noble in nobles]
        for new in nobles_new:
            noble =list(filter(lambda c: c.id == new.id , nobles_origin))
            if noble==[]:
                self._user_sql_session.add(noble)              
