"""Drop column watchlist_name

Revision ID: 9a1e19f2690c
Revises: 6c723283fdca
Create Date: 2023-02-18 16:11:18.532976

"""
from alembic import op
import sqlalchemy as sa
import logging


# revision identifiers, used by Alembic.
revision = '9a1e19f2690c'
down_revision = '6c723283fdca'
branch_labels = None
depends_on = None
alembic_logger = logging.getLogger("alembic")


def upgrade():
    alembic_logger.info("Drop Column watchlist_name.")
    op.execute("""ALTER TABLE push_notification_record DROP COLUMN watchlist_name;""")
    op.execute("""ALTER TABLE push_notification_robo DROP COLUMN watchlist_name;""")


def downgrade():
    alembic_logger.info("Add Column watchlist_name.")
    op.execute(
        """ALTER TABLE push_notification_robo ADD COLUMN watchlist_name VARCHAR(100) NOT NULL COMMENT '追蹤清單名稱' after notification_method;""")
    op.execute(
        """ALTER TABLE push_notification_record ADD COLUMN watchlist_name VARCHAR(100) NOT NULL COMMENT '追蹤清單名稱' after notification_method;""")
