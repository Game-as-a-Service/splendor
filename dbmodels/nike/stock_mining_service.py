from sqlalchemy import DATETIME, Column, String, text, BOOLEAN, DATE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StockMiningService(Base):
    __tablename__ = "stock_mining_service"

    service = Column(String(100, "utf8mb4_unicode_ci"), primary_key=True, comment="服務")
    activity = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="活動")
    is_free_open = Column(BOOLEAN, nullable=False, comment="是否免費開放, True: 免費開放, False: 需訂閱才能使用")
    open_at = Column(DATE, nullable=True, comment="開放時間, is_free_open 為 True: YYYY-MM-DD, False: Null")
    close_at = Column(DATE, nullable=True, comment="結束時間, is_free_open 為 True: YYYY-MM-DD, False: Null")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
