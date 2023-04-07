from sqlalchemy import DATETIME, INTEGER, Column, text, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FamousInvestorStatus(Base):
    __tablename__ = "famous_investor_status"

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    investorname = Column(String(200, "utf8mb4_unicode_ci"), nullable=False, comment="投資機構")
    investorname_zh = Column(String(200, "utf8mb4_unicode_ci"), nullable=False, comment="投資機構（中文）")
    quarter_1 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近一季度")
    units_1 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近一季度單位數")
    units_pct_1 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近一季度變化率")
    quarter_2 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第二個季度")
    units_2 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第二個季度單位數")
    units_pct_2 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第二個季度變化率")
    quarter_3 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第三個季度")
    units_3 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第三個季度單位數")
    units_pct_3 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第三個季度變化率")
    quarter_4 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第四個季度")
    units_4 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第四個季度單位數")
    units_pct_4 = Column(String(20, "utf8mb4_unicode_ci"), nullable=False, comment="最近第四個季度變化率")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
