from sqlalchemy import DATETIME, INTEGER, JSON, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class InstitutionExclusiveOffers(Base):
    __tablename__ = "institution_exclusive_offers"

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    user_id = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="Growin 客戶編號")
    institution = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="機構名稱")
    collaborate = Column(String(50, "utf8mb4_unicode_ci"), nullable=False, comment="合作案")
    package = Column(JSON, nullable=False, comment="優惠內容"
                                                   "minimumOrder: 低消"
                                                   "charge: 手續費")
    start_at = Column(DATETIME, nullable=False, comment="優惠開始時間")
    end_at = Column(DATETIME, nullable=True, comment="優惠結束時間")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
