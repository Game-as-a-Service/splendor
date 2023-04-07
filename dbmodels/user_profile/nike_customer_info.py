from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class NikeCustomerInfo(Base):
    __tablename__ = "nike_customer_info"

    user_id = Column(String(100, "utf8mb4_unicode_ci"), primary_key=True, comment="Growin 客戶編號")
    customer_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="Stripe 客戶編號")
    name = Column(String(500, "utf8mb4_unicode_ci"), nullable=True, comment="客戶姓名")
    phone = Column(String(20, "utf8mb4_unicode_ci"), nullable=True, comment="手機號碼")
    email = Column(String(500, "utf8mb4_unicode_ci"), nullable=True, comment="電子信箱")
    plan = Column(String(50, "utf8mb4_unicode_ci"), nullable=False, comment="方案"
                                                                            "Free: 免費方案"
                                                                            "Basic Yearly: 基本方案（年繳）"
                                                                            "Basic Monthly: 基本方案（月繳）"
                                                                            "Premium Yearly: 進階方案（年繳）"
                                                                            "Premium Monthly: 進階方案（月繳）")
    subscribed_at = Column(DATE, nullable=True, comment="訂閱日期")
    expire_at = Column(DATE, nullable=True, comment="到期日期")
    status = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="Stripe 客戶訂閱狀態"
                                                                              "inactive: 待用"
                                                                              "trialing: 適用期"
                                                                              "active: 正式使用"
                                                                              "canceled: 已取消")
    watchlist_index = Column(TINYINT, nullable=False, default=0, comment="上次瀏覽的追蹤清單 index")
    watchlist = Column(JSON, nullable=False, comment="追蹤清單")
    use_tag = Column(BOOLEAN, nullable=False, default=False, comment="使用服務")
    line_user_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=True, comment="LINE 使用者編號")
    line_nonce = Column(String(500, "utf8mb4_unicode_ci"), nullable=True, comment="LINE Nonce")
    line_bind_status = Column(BOOLEAN, nullable=True, default=0, comment="LINE 綁定狀態")
    line_bind_at = Column(DATETIME, nullable=True, comment="LINE 綁定時間")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
