from sqlalchemy import DATE, DATETIME, DECIMAL, INTEGER, Column, Index, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StripeSubscribeInfo(Base):
    __tablename__ = "stripe_subscribe_info"
    __table_args__ = (
        Index("customer_id", "customer_id", unique=False),
        Index("subscription_id", "subscription_id", unique=False),
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    subscription_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Stripe 訂閱編號")
    customer_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Stripe 客戶編號")
    price_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Stripe 產品編號")
    plan = Column(String(50, "utf8mb4_unicode_ci"), nullable=False, comment="方案")
    currency = Column(String(3, "utf8mb4_unicode_ci"), nullable=False, comment="幣別")
    discount = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="折價券")
    exp_month = Column(INTEGER, nullable=True, comment="信用卡有效月份")
    exp_year = Column(INTEGER, nullable=True, comment="信用卡有效年份")
    last_four = Column(String(4, "utf8mb4_unicode_ci"), nullable=True, comment="信用卡後四碼")
    total = Column(DECIMAL(12, 2), nullable=False, comment="總支付金額")
    receipt_pdf_link = Column(String(1000, "utf8mb4_unicode_ci"), nullable=False, comment="收據連結")
    invoice_number = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="帳單號碼")
    receipt_number = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="收據號碼")
    subscribed_at = Column(DATE, nullable=False, comment="訂閱日期")
    expire_at = Column(DATE, nullable=False, comment="到期日期")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
