from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TableInfo(Base):
    __tablename__ = "table_info"    

    game_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="遊戲編號")
    table_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="桌面編號")
    diamond = Column(Integer, nullable=False, comment="鑽石")
    sapphire = Column(Integer, nullable=False, comment="藍寶石")
    emerald = Column(Integer, nullable=False, comment="綠寶石")
    ruby = Column(Integer, nullable=False, comment="紅寶石")
    onyx = Column(Integer, nullable=False, comment="瑪瑙")
    gold = Column(Integer, nullable=False, comment="黃金")
