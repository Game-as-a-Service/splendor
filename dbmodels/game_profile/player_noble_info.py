from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from domain import Noble

Base = declarative_base()
metadata = Base.metadata


class PlayerNobleInfo(Base):
    __tablename__ = "player_noble_info"    

    game_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="遊戲編號")
    player_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="玩家編號")
    noble_id = Column(Integer, primary_key=True, comment="貴族卡編號")

    @classmethod
    def from_noble(cls, noble: Noble,game_id:str,player_id:str) -> "PlayerNobleInfo":
        return cls(
            game_id =game_id,
            player_id =player_id,
            noble_id=noble.id,
        )