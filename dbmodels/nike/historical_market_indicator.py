from sqlalchemy import DATETIME, DATE, INTEGER, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class HistoricalMarketIndicator(Base):
    __tablename__ = "historical_market_indicator"

    id = Column(INTEGER, primary_key=True, comment="流水號")
    indicator = Column(String(45, "utf8mb4_unicode_ci"), nullable=False, comment="指標")
    date = Column(DATE, nullable=False, comment="日期")
    value = Column(INTEGER, nullable=False, comment="數值")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP"), comment="資料建立時間")
