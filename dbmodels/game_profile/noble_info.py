from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON,Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()
metadata = Base.metadata

@dataclass
class NobleInfo(Base):
    __tablename__ = "noble_info"    

    noble_id = Column(Integer, primary_key=True, comment="貴族卡編號")
    score = Column(Integer, nullable=False, comment="分數")
    diamond = Column(Integer, nullable=False, comment="鑽石")
    sapphire = Column(Integer, nullable=False, comment="藍寶石")
    emerald = Column(Integer, nullable=False, comment="綠寶石")
    ruby = Column(Integer, nullable=False, comment="紅寶石")
    onyx = Column(Integer, nullable=False, comment="瑪瑙")
