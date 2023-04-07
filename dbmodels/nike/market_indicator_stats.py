from sqlalchemy import DATETIME, DECIMAL, INTEGER, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MarketIndicatorStats(Base):
    __tablename__ = "market_indicator_stats"

    id = Column(INTEGER, primary_key=True, comment="流水號")
    indicator = Column(String(45), nullable=False, comment="指標名稱")
    indicator_status = Column(String(45), nullable=False, comment="指標狀態")
    profitability = Column(DECIMAL(40, 5), nullable=False, comment="上漲比率")
    avg_profit_and_loss = Column(DECIMAL(40, 5), nullable=False, comment="平均損益")
    avg_profit = Column(DECIMAL(40, 5), nullable=True, comment="平均上漲")
    avg_loss = Column(DECIMAL(40, 5), nullable=True, comment="平均下跌")
    quantile_25 = Column(DECIMAL(40, 5), nullable=False, comment="25 百分位")
    quantile_50 = Column(DECIMAL(40, 5), nullable=False, comment="50 百分位")
    quantile_75 = Column(DECIMAL(40, 5), nullable=False, comment="75 百分位")
    min = Column(DECIMAL(40, 5), nullable=True, comment="最小值")
    max = Column(DECIMAL(40, 5), nullable=True, comment="最大值")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP"), comment="資料建立時間")
