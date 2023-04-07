from sqlalchemy import BIGINT, DATETIME, Column, String, JSON, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PushNotificationRobo(Base):
    __tablename__ = "push_notification_robo"

    id = Column(BIGINT, primary_key=True, comment="id")
    user_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Growin 客戶編號")
    strategy_name = Column(String(50, "utf8mb4_unicode_ci"), nullable=False, comment="策略名稱")
    strategy_category = Column(String(4, "utf8mb4_unicode_ci"), nullable=False, comment="進場 BUY"
                                                                                        "出場 SELL")
    status = Column(String(8, "utf8mb4_unicode_ci"), nullable=False, comment="狀態"
                                                                             "啟用中 active"
                                                                             "停用中 inactive")
    setting_type = Column(String(10, "utf8mb4_unicode_ci"), nullable=False, comment="設定類型"
                                                                                    "自訂 self-robo"
                                                                                    "價值機器人 value-robo"
                                                                                    "波段機器人 swing-robo"
                                                                                    "趨勢機器人 trend-robo")
    notification_method = Column(String(5, "utf8mb4_unicode_ci"), nullable=False, comment="通知方式"
                                                                                          "Email"
                                                                                          "Line")
    symbols = Column(JSON, nullable=False, comment="追蹤標的列表")
    details = Column(JSON, nullable=False, comment="策略細節")
    finished_at = Column(DATETIME, nullable=False, comment="偵測結束時間")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
