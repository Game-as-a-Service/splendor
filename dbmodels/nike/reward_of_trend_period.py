from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, Index, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RewardOfTrendPeriod(Base):
    __tablename__ = "reward_of_trend_period"
    __table_args__ = (
        Index("index_symbol_column", "symbol", unique=False),
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    score = Column(INTEGER, nullable=False, comment="分數")
    occurrence = Column(INTEGER, nullable=True, comment="發生次數")
    avg_profit_and_loss = Column(DECIMAL(40, 12), nullable=True, comment="平均期間報酬")
    profits = Column(INTEGER, nullable=True, comment="上漲次數")
    profitability = Column(DECIMAL(40, 12), nullable=True, comment="上漲比率")
    avg_profit = Column(DECIMAL(40, 12), nullable=True, comment="平均上漲幅度")
    avg_loss = Column(DECIMAL(40, 12), nullable=True, comment="平均下降幅度")
    avg_holding_time = Column(DECIMAL(40, 12), nullable=True, comment="平均期間天數")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
