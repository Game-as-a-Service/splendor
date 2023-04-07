from sqlalchemy import DATETIME, INTEGER, JSON, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CancelSubscribeRecord(Base):
    __tablename__ = "cancel_subscribe_record"

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    subscription_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="訂閱編號")
    customer_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Stripe客戶編號")
    canceled_at = Column(DATETIME, nullable=True, comment="提出取消時間")
    expire_at = Column(DATETIME, nullable=True, comment="到期日期")
    reason = Column(JSON, nullable=True, comment="原因")
    recovered_at = Column(DATETIME, nullable=True, comment="恢復訂閱時間")
    status = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="狀態"
                                                                              "canceled: 取消訂閱"
                                                                              "recovered: 恢復訂閱")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
