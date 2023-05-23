from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

from application.user_case import PlayerUserCase

Base = declarative_base()
metadata = Base.metadata


class PlayerInfo(Base):
    __tablename__ = "player_info"    

    game_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="遊戲編號")
    player_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="玩家編號")
    seq = Column(Integer, nullable=False, comment="順序")
    score = Column(Integer, nullable=False, comment="分數")
    diamond = Column(Integer, nullable=False, comment="鑽石")
    sapphire = Column(Integer, nullable=False, comment="藍寶石")
    emerald = Column(Integer, nullable=False, comment="綠寶石")
    ruby = Column(Integer, nullable=False, comment="紅寶石")
    onyx = Column(Integer, nullable=False, comment="瑪瑙")
    gold = Column(Integer, nullable=False, comment="黃金")
    bonus_diamond = Column(Integer, nullable=False, comment="永久鑽石")
    bonus_sapphire = Column(Integer, nullable=False, comment="永久藍寶石")
    bonus_emerald = Column(Integer, nullable=False, comment="永久綠寶石")
    bonus_ruby = Column(Integer, nullable=False, comment="永久紅寶石")
    bonus_onyx = Column(Integer, nullable=False, comment="永久瑪瑙")


    @classmethod
    def update(cls,orgin:"PlayerInfo",new:PlayerUserCase)->"PlayerInfo":
        return cls(
            game_id=orgin.game_id,
            player_id = orgin.player_id,
            seq = orgin.seq,
            score = new.score,
            diamond =new.resource.diamond,
            sapphire =new.resource.sapphire,
            emerald =new.resource.emerald,
            ruby =new.resource.ruby,
            onyx =new.resource.onyx,
            gold =new.resource.gold,
            bonus_diamond = new.bonus.diamond,
            bonus_sapphire = new.bonus.sapphire,
            bonus_emerald = new.bonus.emerald,
            bonus_ruby = new.bonus.ruby,
            bonus_onyx = new.bonus.onyx,
        )