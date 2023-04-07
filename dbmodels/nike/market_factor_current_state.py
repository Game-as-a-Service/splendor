from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, Index, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MarketFactorCurrentState(Base):
    __tablename__ = "market_factor_current_state"

    id = Column(INTEGER, primary_key=True, comment="流水號")
    factor = Column(String(45, "utf8mb4_unicode_ci"), nullable=False, comment="因子名稱")
    indicator = Column(String(45, "utf8mb4_unicode_ci"), nullable=False, comment="指標名稱")
    factor_condition = Column(INTEGER, nullable=False, comment="因子狀態")
    frequency = Column(String(1, "utf8mb4_unicode_ci"), nullable=False, comment="頻率")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
