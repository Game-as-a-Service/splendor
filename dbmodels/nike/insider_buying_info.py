from sqlalchemy import DATETIME, INTEGER, Column, Index, text, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class InsiderBuyingInfo(Base):
    __tablename__ = "insider_buying_info"
    __table_args__ = (
        Index("index_symbol_column", "symbol", unique=False),
        Index("index_filling_date_column", "filing_date", unique=False),
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    filing_date = Column(DATETIME, nullable=False, comment="申報日期")
    buyer_name = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="購買人")
    buyer_title = Column(String(30, "utf8mb4_unicode_ci"), nullable=True, comment="購買人職稱")
    trade_date = Column(DATETIME, nullable=True, comment="交易日")
    trade_num = Column(INTEGER, nullable=True, comment="交易股數")
    trade_cash = Column(INTEGER, nullable=True, comment="交易金額")
    trade_num_after = Column(INTEGER, nullable=True, comment="交易後持股數")
    stock_category = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="股票類型")
    stock_category_zh = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="股票類型(中文)")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
