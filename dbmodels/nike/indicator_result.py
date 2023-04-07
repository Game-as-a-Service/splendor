from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, Index, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class IndicatorResult(Base):
    __tablename__ = "indicator_result"
    __table_args__ = (
        Index("index_symbol_column", "symbol", unique=False),
        Index("index_date_column", "date", unique=False),
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    date = Column(DATETIME, nullable=False, comment="日期")
    indicator = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="因子")
    value = Column(DECIMAL(40, 12), nullable=False, comment="數值")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
