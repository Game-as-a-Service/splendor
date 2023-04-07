from sqlalchemy import DATETIME, INTEGER, Column, String, text, JSON, DATE, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class VideoInfo(Base):
    __tablename__ = "video_info"

    id = Column(INTEGER, primary_key=True, comment="流水號（pk）")
    category = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="類別"
                                                                                 "market-analysis: 市場分析"
                                                                                 "oriented-analysis: 五力分析"
                                                                                 "finance-knowledge: 金融知識")
    title = Column(String(100, "utf8mb4_unicode_ci"), nullable=False, comment="標題")
    content = Column(String(10000, "utf8mb4_unicode_ci"), nullable=False, comment="內文")
    symbol = Column(JSON, nullable=True, comment="標的列表")
    published_at = Column(DATE, nullable=False, comment="影片發布時間")
    photo_url = Column(String(500, "utf8mb4_unicode_ci"), nullable=False, comment="封面照 URL")
    video_url = Column(String(500, "utf8mb4_unicode_ci"), nullable=False, comment="影片 URL")
    status = Column(BOOLEAN, nullable=False, comment="開放狀態")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
