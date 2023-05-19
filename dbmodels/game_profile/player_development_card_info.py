from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from domain import DevelopmentCard

Base = declarative_base()
metadata = Base.metadata


class PlayerDevelopmentCardInfo(Base):
    __tablename__ = "player_development_card_info"    

    game_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="遊戲編號")
    player_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="玩家編號")
    level = Column(Integer, primary_key=True, comment="level")
    id = Column(Integer, primary_key=True, comment="id")
    status = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="狀態(buy,reserve)")

    @classmethod
    def from_development_card(cls, development_card: DevelopmentCard,game_id:str,player_id:str,is_buy:bool) -> "PlayerDevelopmentCardInfo":
        return cls(
            game_id =game_id,
            player_id =player_id,
            level=development_card.level,
            id=development_card.id,
            status = 'buy' if is_buy else 'reserve'
        
        )