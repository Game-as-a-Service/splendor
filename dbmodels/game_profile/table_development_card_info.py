from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TableDevelopmentCardInfo(Base):
    __tablename__ = "table_development_card_info"    

    game_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="遊戲編號")
    table_id = Column(String(36, "utf8mb4_unicode_ci"), primary_key=True, comment="桌面編號")
    level = Column(Integer, primary_key=True, comment="level")
    id = Column(Integer, primary_key=True, comment="id")
    seq = Column(Integer, nullable=False, comment="順序")
    status = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="狀態(indeck,ontable")
