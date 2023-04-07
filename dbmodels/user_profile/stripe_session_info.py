from sqlalchemy import DATETIME, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StripeSessionInfo(Base):
    __tablename__ = "stripe_session_info"

    session_id = Column(String(100, "utf8mb4_unicode_ci"), primary_key=True, comment="訂單 Session 編號")
    payment_status = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="付款狀態"
                                                                                      "unpaid: 待處理"
                                                                                      "paid: 付款成功")
    user_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Growin 客戶編號")
    customer_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="Stripe 客戶編號")
    subscription_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="Stripe 訂單編號")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
