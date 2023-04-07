from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SymbolMapping(Base):
    __tablename__ = "symbol_mapping"

    symbol = Column(String(30, "utf8mb4_unicode_ci"), primary_key=True, nullable=False, comment="標的")
    target_symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="對應的標的")
