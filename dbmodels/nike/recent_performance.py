from sqlalchemy import DATETIME, DECIMAL, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RecentPerformance(Base):
    __tablename__ = "recent_performance"

    symbol = Column(String(30, "utf8mb4_unicode_ci"), primary_key=True, nullable=False, comment="標的名稱")
    _1d_return = Column(DECIMAL(40, 12), nullable=True, comment="一日報酬率")
    _5d_return = Column(DECIMAL(40, 12), nullable=True, comment="近五日報酬率")
    _1m_return = Column(DECIMAL(40, 12), nullable=True, comment="近一月報酬率")
    _3m_return = Column(DECIMAL(40, 12), nullable=True, comment="近三月報酬率")
    _6m_return = Column(DECIMAL(40, 12), nullable=True, comment="近半年報酬率")
    _1y_return = Column(DECIMAL(40, 12), nullable=True, comment="近一年報酬率")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
