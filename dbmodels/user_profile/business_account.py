from sqlalchemy import DATETIME, JSON, Column, String, text, BOOLEAN, DATE
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BusinessAccount(Base):
    __tablename__ = "business_account"

    user_id = Column(String(100, "utf8mb4_unicode_ci"), primary_key=True, comment="企業帳號")
    password = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="密碼")
    company = Column(String(50, "utf8mb4_unicode_ci"), nullable=False, comment="企業名稱")
    company_code = Column(String(50, "utf8mb4_unicode_ci"), nullable=False, comment="企業代號")
    status = Column(BOOLEAN, nullable=False, comment="狀態"
                                                     "True: 可使用,"
                                                     "False: 不可使用")
    plan = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="方案"
                                                                            "Basic Yearly: 基本方案（年繳）"
                                                                            "Basic Monthly: 基本方案（月繳）"
                                                                            "Premium Yearly: 進階方案（年繳）"
                                                                            "Premium Monthly: 進階方案（月繳）")
    subscribed_at = Column(DATE, nullable=True, comment="訂閱日期")
    expire_at = Column(DATE, nullable=True, comment="到期日期")
    watchlist_index = Column(TINYINT, nullable=False, default=0, comment="上次瀏覽的追蹤清單 index")
    watchlist = Column(JSON, nullable=False, comment="追蹤清單")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
