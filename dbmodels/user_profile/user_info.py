from sqlalchemy import DATE, DATETIME, Column, String, text, BOOLEAN, JSON
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(String(100, "utf8mb4_unicode_ci"), primary_key=True, comment="客戶編號")
    name = Column(String(500, "utf8mb4_unicode_ci"), nullable=True, comment="客戶姓名")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")

    def __repr__(self):
        return f"UserInfo(user_id={self.user_id}, name={self.name}, updated_at={self.updated_at}, created_at={self.created_at})"
