"""create userinfo table

Revision ID: c688d28a6fe3
Revises: 
Create Date: 2023-04-08 23:57:03.216424

"""
from alembic import op
import logging


# revision identifiers, used by Alembic.
revision = 'c688d28a6fe3'
down_revision = None
branch_labels = None
depends_on = None
alembic_logger = logging.getLogger('alembic')

def upgrade():
    alembic_logger.info("Create Table userinfo.")
    stm = """
        CREATE TABLE user_info (
            user_id VARCHAR(100) NOT NULL COMMENT '客戶編號',
            name VARCHAR(500) NOT NULL COMMENT '客戶姓名',
            updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
            PRIMARY KEY (user_id));
    """
    op.execute(stm)


def downgrade():
    alembic_logger.info("Drop Table user_info;")
    op.execute("""DROP TABLE user_info;""")