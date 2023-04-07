from sqlalchemy import DATETIME, INTEGER, Column, String, text, DECIMAL, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MarketSignalList(Base):
    __tablename__ = "market_signal_list"

    indicator = Column(String(45, "utf8_unicode_ci"), primary_key=True, comment="指標名稱")
    start_at = Column(DATETIME, primary_key=True, comment="發生日期")
    end_at = Column(DATETIME, primary_key=True, comment="結束日期")
    value = Column(INTEGER, nullable=False, comment="指標")
    duration = Column(INTEGER, nullable=False, comment="期間天數")
    cum_return = Column(DECIMAL(40, 4), nullable=False, comment="期間報酬")
    max_drawdown = Column(DECIMAL(40, 4), nullable=False, comment="期間最大跌幅")
    event = Column(TEXT, nullable=True, comment="對應事件")
    event_en = Column(TEXT, nullable=True, comment="對應事件（英文）")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
