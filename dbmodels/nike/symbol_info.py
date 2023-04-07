from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SymbolInfo(Base):
    __tablename__ = "symbol_info"

    symbol = Column(String(30, "utf8mb4_unicode_ci"), primary_key=True, nullable=False, comment="標的名稱")
    name = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="標的全名")
    exchange = Column(String(10, "utf8mb4_unicode_ci"), nullable=True, comment="交易所")
    country = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="國家")
    price = Column(DECIMAL(40, 12), nullable=False, comment="股價")
    value = Column(INTEGER, nullable=True, comment="目前價值評分")
    trend = Column(INTEGER, nullable=True, comment="目前趨勢評分")
    swing = Column(INTEGER, nullable=True, comment="目前波段評分")
    dividend = Column(INTEGER, nullable=True, comment="目前股利評分")
    chip = Column(INTEGER, nullable=True, comment="目前籌碼評分")
    main_category_id = Column(String(50, "utf8mb4_unicode_ci"), nullable=True, comment="大分類編號")
    main_category = Column(String(50, "utf8mb4_unicode_ci"), nullable=True, comment="大分類")
    sub_category_id = Column(String(50, "utf8mb4_unicode_ci"), nullable=True, comment="子分類編號")
    sub_category = Column(String(50, "utf8mb4_unicode_ci"), nullable=True, comment="子分類")
    main_category_zh_tw = Column(String(50, "utf8mb4_unicode_ci"), nullable=True, comment="大分類(中文)")
    sub_category_zh_tw = Column(String(50, "utf8mb4_unicode_ci"), nullable=True, comment="子分類(中文)")
    market_cap = Column(DECIMAL(40, 12), nullable=True, comment="市值")
    volume = Column(DECIMAL(40, 12), nullable=True, comment="當日交易量")
    volume_20MA = Column(DECIMAL(40, 12), nullable=True, comment="20 日平均交易量")
    power_squeeze_daily = Column(DECIMAL(40, 12), nullable=True, comment="power_squeeze_daily")
    power_squeeze_weekly = Column(DECIMAL(40, 12), nullable=True, comment="power_squeeze_weekly")
    surfing_trend_daily = Column(DECIMAL(40, 12), nullable=True, comment="surfing_trend_daily")
    surfing_trend_weekly = Column(DECIMAL(40, 12), nullable=True, comment="surfing_trend_weekly")
    summary = Column(String(500, "utf8mb4_unicode_ci"), nullable=True, comment="評價總結")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
