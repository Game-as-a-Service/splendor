from sqlalchemy import DATETIME, INTEGER, Column, DECIMAL, String, text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AiPredict(Base):
    __tablename__ = "ai_predict"
    __table_args__ = {
        "mysql_partition_by": """
            PARTITION BY RANGE(YEAR(date)) (
                PARTITION p1994 VALUES LESS THAN (1995),
                PARTITION p1995 VALUES LESS THAN (1996),
                PARTITION p1996 VALUES LESS THAN (1997),
                PARTITION p1997 VALUES LESS THAN (1998),
                PARTITION p1998 VALUES LESS THAN (1999),
                PARTITION p1999 VALUES LESS THAN (2000),
                PARTITION p2000 VALUES LESS THAN (2001),
                PARTITION p2001 VALUES LESS THAN (2002),
                PARTITION p2002 VALUES LESS THAN (2003),
                PARTITION p2003 VALUES LESS THAN (2004),
                PARTITION p2004 VALUES LESS THAN (2005),
                PARTITION p2005 VALUES LESS THAN (2006),
                PARTITION p2006 VALUES LESS THAN (2007),
                PARTITION p2007 VALUES LESS THAN (2008),
                PARTITION p2008 VALUES LESS THAN (2009),
                PARTITION p2009 VALUES LESS THAN (2010),
                PARTITION p2010 VALUES LESS THAN (2011),
                PARTITION p2011 VALUES LESS THAN (2012),
                PARTITION p2012 VALUES LESS THAN (2013),
                PARTITION p2013 VALUES LESS THAN (2014),
                PARTITION p2014 VALUES LESS THAN (2015),
                PARTITION p2015 VALUES LESS THAN (2016),
                PARTITION p2016 VALUES LESS THAN (2017),
                PARTITION p2017 VALUES LESS THAN (2018),
                PARTITION p2018 VALUES LESS THAN (2019),
                PARTITION p2019 VALUES LESS THAN (2020),
                PARTITION p2020 VALUES LESS THAN (2021),
                PARTITION p2021 VALUES LESS THAN (2022),
                PARTITION p2022 VALUES LESS THAN (2023),
                PARTITION p2023 VALUES LESS THAN (2024),
                PARTITION p2024 VALUES LESS THAN (2025),
                PARTITION p2025 VALUES LESS THAN (2026),
                PARTITION p2026 VALUES LESS THAN (2027),
                PARTITION p2027 VALUES LESS THAN (2028),
                PARTITION p2028 VALUES LESS THAN (2029),
                PARTITION p2029 VALUES LESS THAN (2030),
                PARTITION p2030 VALUES LESS THAN (2031)
            );
        """
    }
    __table_args__ = (
        Index("index_symbol_column", "symbol", unique=False),
        Index("index_date_column", "date", unique=False),
    )

    id = Column(INTEGER, primary_key=True, comment="流水號 (pk)")
    symbol = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="標的名稱")
    date = Column(DATETIME, nullable=False, comment="日期")
    oriented = Column(String(30, "utf8mb4_unicode_ci"), nullable=False, comment="面向")
    signal = Column(DECIMAL(40, 12), nullable=True, comment="訊號")
    updated_at = Column(DATETIME, nullable=True, server_default=text(
        'NULL ON UPDATE CURRENT_TIMESTAMP'), comment="資料更新時間")
    created_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="資料建立時間")
