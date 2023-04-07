from sqlalchemy import DATETIME, DATE, INTEGER, Column, String, text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class HistoricalMarketFactor(Base):
    __tablename__ = "historical_market_factor"

    id = Column(INTEGER, primary_key=True, comment="流水號")
    factor = Column(String(45, "utf8mb4_unicode_ci"), nullable=False, comment="因子名稱")
    indicator = Column(String(45, "utf8mb4_unicode_ci"), nullable=False, comment="指標名稱")
    date = Column(DATE, nullable=False, comment="日期")
    value = Column(DECIMAL(40, 5), nullable=False, comment="數值")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP"), comment="資料建立時間")
