from sqlalchemy import DATETIME, INTEGER, Column, Index, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ChipBasicInfo(Base):
    __tablename__ = "chip_basic_info"
    __table_args__ = (
        Index("index_symbol_column", "symbol", unique=False),
        Index("index_date_column", "date", unique=False)
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    date = Column(DATETIME, nullable=False, comment="日期")
    cash_surplus = Column(INTEGER, nullable=True, comment="資金淨增")
    cash_net_in = Column(INTEGER, nullable=True, comment="資金流入")
    cash_net_out = Column(INTEGER, nullable=True, comment="資金流出")
    add_inst_num = Column(INTEGER, nullable=True, comment="加碼_間數")
    add_total_cash = Column(INTEGER, nullable=True, comment="加碼_金額")
    build_inst_num = Column(INTEGER, nullable=True, comment="建倉_間數")
    build_total_cash = Column(INTEGER, nullable=True, comment="建倉_金額")
    reduce_inst_num = Column(INTEGER, nullable=True, comment="減碼_間數")
    reduce_total_cash = Column(INTEGER, nullable=True, comment="減碼_金額")
    clean_inst_num = Column(INTEGER, nullable=True, comment="清倉_間數")
    clean_total_cash = Column(INTEGER, nullable=True, comment="清倉_金額")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
