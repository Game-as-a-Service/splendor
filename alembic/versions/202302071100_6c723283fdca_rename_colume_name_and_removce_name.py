"""Rename Colume Name and Removce Name

Revision ID: 6c723283fdca
Revises: a93d46d892be
Create Date: 2023-02-07 11:00:28.496114

"""
import logging

from alembic import op

# revision identifiers, used by Alembic.
revision = '6c723283fdca'
down_revision = 'a93d46d892be'
branch_labels = None
depends_on = None
alembic_logger = logging.getLogger("alembic")


def upgrade():
    alembic_logger.info("push_notification_robo rename watchlist to watchlist_name.")
    op.execute(
        """ALTER TABLE push_notification_robo CHANGE COLUMN watchlist watchlist_name VARCHAR(100) NOT NULL COMMENT '追蹤清單名稱';""")

    alembic_logger.info("push_notification_robo remove watchlistId.")
    op.execute("""ALTER TABLE push_notification_robo DROP COLUMN watchlist_id;""")

    alembic_logger.info("push_notification_record rename watchlist to watchlist_name.")
    op.execute(
        """ALTER TABLE push_notification_record CHANGE COLUMN watchlist watchlist_name VARCHAR(100) NOT NULL COMMENT '追蹤清單名稱';""")

    alembic_logger.info("push_notification_record remove watchlistId.")
    op.execute("""ALTER TABLE push_notification_record DROP COLUMN watchlist_id;""")


def downgrade():
    alembic_logger.info("push_notification_robo rename watchlist_name to watchlist.")
    op.execute(
        """ALTER TABLE push_notification_robo CHANGE COLUMN watchlist_name watchlist VARCHAR(100) NOT NULL COMMENT '追蹤清單名稱';""")

    alembic_logger.info("push_notification_robo add watchlistId.")
    op.execute(
        """ALTER TABLE push_notification_robo ADD COLUMN watchlist_id VARCHAR(32) NOT NULL COMMENT '追蹤清單編號' after watchlist;""")

    alembic_logger.info("push_notification_record rename watchlist_name to watchlist.")
    op.execute(
        """ALTER TABLE push_notification_record CHANGE COLUMN watchlist_name watchlist VARCHAR(100) NOT NULL COMMENT '追蹤清單名稱';""")

    alembic_logger.info("push_notification_record add watchlistId.")
    op.execute(
        """ALTER TABLE push_notification_record ADD COLUMN watchlist_id VARCHAR(32) NOT NULL COMMENT '追蹤清單編號' after watchlist;""")
