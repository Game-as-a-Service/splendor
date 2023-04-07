from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, Index, text, String, DATE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BacktestResult(Base):
    __tablename__ = "backtest_result"
    __table_args__ = (
        Index("index_version_column", "version", unique=False),
        Index("index_symbol_column", "symbol", unique=False)
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    oriented = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="面向")
    version = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="版號")
    strategy = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="進出場策略")
    occurrence = Column(INTEGER, nullable=True, comment="發生次數")
    profits = Column(INTEGER, nullable=True, comment="獲利次數")
    profitability = Column(DECIMAL(40, 12), nullable=True, comment="獲利機率")
    avg_profit_and_loss = Column(DECIMAL(40, 12), nullable=True, comment="平均損益")
    avg_profit = Column(DECIMAL(40, 12), nullable=True, comment="平均獲利")
    avg_loss = Column(DECIMAL(40, 12), nullable=True, comment="平均損益")
    avg_profit_to_loss_ratio = Column(DECIMAL(40, 12), nullable=True, comment="平均賺賠比")
    quantile_25 = Column(DECIMAL(40, 12), nullable=True, comment="quantile_25")
    quantile_50 = Column(DECIMAL(40, 12), nullable=True, comment="quantile_50")
    quantile_75 = Column(DECIMAL(40, 12), nullable=True, comment="quantile_75")
    avg_holding_time = Column(DECIMAL(40, 12), nullable=True, comment="平均持有時間")
    start_at = Column(DATE, nullable=False, comment="資料起始日期")
    end_at = Column(DATE, nullable=False, comment="資料結束日期")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
