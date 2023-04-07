from sqlalchemy import BIGINT, DATE, Column, DECIMAL, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SECForm13F(Base):
    __tablename__ = "SECForm13F"

    id = Column(BIGINT, primary_key=True)
    ticker = Column(String(10, "utf8_general_ci"), nullable=False)
    investorname = Column(String(150, "utf8_general_ci"), nullable=False)
    securitytype = Column(String(20, "utf8_general_ci"), nullable=False)
    calendardate = Column(DATE, nullable=False)
    value = Column(BIGINT, nullable=False)
    units = Column(BIGINT, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    style = Column(String(150, "utf8_general_ci"), nullable=False)
    weight_pct = Column(DECIMAL(7, 2), nullable=False)
    investorname_alt = Column(String(150, "utf8_general_ci"), nullable=False)
    units_pct = Column(DECIMAL(7, 2), nullable=False)
