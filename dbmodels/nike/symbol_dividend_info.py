from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SymbolDividendInfo(Base):
    __tablename__ = "symbol_dividend_info"

    symbol = Column(String(30, "utf8mb4_unicode_ci"), primary_key=True, nullable=False, comment="標的名稱")
    dividend_yield = Column(DECIMAL(40, 12), nullable=True, comment="平均殖利率")
    filled_days = Column(DECIMAL(40, 12), nullable=True, comment="平均填權息花費日數")
    filled_ratio = Column(DECIMAL(40, 12), nullable=True, comment="填權息率")
    continuous_year = Column(INTEGER, nullable=True, comment="股利連續分派年數")
    volatility = Column(DECIMAL(40, 12), nullable=True, comment="波動率")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
