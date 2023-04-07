from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, Index, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MarketIndicatorCurrentState(Base):
    __tablename__ = "market_indicator_current_state"

    id = Column(INTEGER, primary_key=True, comment="流水號")
    indicator = Column(String(45, "utf8mb4_unicode_ci"), nullable=False, comment="指標名稱")
    value = Column(INTEGER, nullable=False, comment="數值")
    description = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="指標描述")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP"), comment="資料建立時間")
