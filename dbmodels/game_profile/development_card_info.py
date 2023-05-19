from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DevelopmentCardInfo(Base):
    __tablename__ = "development_card_info"    

    level = Column(Integer, primary_key=True, comment="level")
    id = Column(Integer, primary_key=True, comment="id")
    score = Column(Integer, nullable=False, comment="分數")
    diamond = Column(Integer, nullable=False, comment="鑽石")
    sapphire = Column(Integer, nullable=False, comment="藍寶石")
    emerald = Column(Integer, nullable=False, comment="綠寶石")
    ruby = Column(Integer, nullable=False, comment="紅寶石")
    onyx = Column(Integer, nullable=False, comment="瑪瑙")
    bonus = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="獲得寶石")
