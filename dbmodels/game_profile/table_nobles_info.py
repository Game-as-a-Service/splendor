from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TableNoblesInfo(Base):
    __tablename__ = "table_nobles_info"    

    game_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="遊戲編號")
    table_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="桌面編號")
    noble_id = Column(Integer, primary_key=True, comment="貴族卡編號")
    seq = Column(Integer, nullable=False, comment="順序")
