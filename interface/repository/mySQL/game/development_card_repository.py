from typing import Optional

from flask import session
from sqlalchemy.orm import Session,joinedload

from dbmodels.game_profile import PlayerDevelopmentCardInfo,DevelopmentCardInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation
from application.user_case import DevelopmentCardUserCase,ResourceUserCase,TokenUserCase
from typing import List

class DevelopmentCardRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session
    
    def get_development_card_info_by_id(self,level:int,id:int)-> DevelopmentCardUserCase:    
        query =(self._user_sql_session.query(DevelopmentCardInfo)
                .filter(DevelopmentCardInfo.level == level ,
                        DevelopmentCardInfo.id == id)
                            .first())
        return DevelopmentCardUserCase(query.id, query.level,query.score,ResourceUserCase(query.diamond,query.sapphire,query.emerald,query.ruby,query.onyx),TokenUserCase(query.bonus))

    @staticmethod
    def get_player_development_card_info_by_id(self, game_id: str, player_id: str,is_buy:bool)->List[DevelopmentCardUserCase]:
        status = 'buy' if is_buy else 'reserve'
        development_card_info:List[DevelopmentCardInfo] =(self._user_sql_session
                            .query(DevelopmentCardInfo)
                            .join(PlayerDevelopmentCardInfo, (PlayerDevelopmentCardInfo.level == DevelopmentCardInfo.level) &
                                (PlayerDevelopmentCardInfo.id == DevelopmentCardInfo.id),isouter=True)
                            .filter(PlayerDevelopmentCardInfo.game_id == game_id , PlayerDevelopmentCardInfo.player_id == player_id , PlayerDevelopmentCardInfo.status==status)
                            .all())
     
        return [DevelopmentCardUserCase.to_usercase(card.level, card.id,card.score, ResourceUserCase.to_usercase(card.diamond, card.sapphire, card.emerald, card.ruby, card.onyx),TokenUserCase[card.bonus]) for card in development_card_info]

    @staticmethod
    def set_player_development_card_info_by_id(self, game_id: str, player_id: str,cards:List[DevelopmentCardUserCase],is_buy:bool)->None:
        status = 'buy' if is_buy else 'reserve'
        development_card_info_origin:List[PlayerDevelopmentCardInfo] =(self._user_sql_session
                            .query(PlayerDevelopmentCardInfo)
                            .join(DevelopmentCardInfo, (PlayerDevelopmentCardInfo.level == DevelopmentCardInfo.level) &
                                (PlayerDevelopmentCardInfo.id == DevelopmentCardInfo.id))
                            .filter(PlayerDevelopmentCardInfo.game_id == game_id , PlayerDevelopmentCardInfo.player_id == player_id , PlayerDevelopmentCardInfo.status==status)
                            .all())

        cards_new =[PlayerDevelopmentCardInfo.from_development_card(card,game_id,player_id,is_buy) for card in cards]

        for orgin in development_card_info_origin:
            card =list(filter(lambda c:c.level == orgin.level and c.id == orgin.id , cards_new))
            if card==[]:
                self._user_sql_session.delete(orgin)                
            else:
                cards_new.remove(card[0])

        for card in cards_new:
            self._user_sql_session.add(card)


        
