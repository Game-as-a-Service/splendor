from sqlalchemy import DATETIME, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TradingviewAccountList(Base):
    __tablename__ = "tradingview_account_list"

    user_id = Column(String(100, "utf8mb4_unicode_ci"), primary_key=True, comment="Growin 客戶編號")
    tradingview_account = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="TradingView 帳號")
    last_tradingview_account = Column(String(100, "utf8mb4_unicode_ci"), nullable=True,
                                      comment="上次登記的TradingView 帳號")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
