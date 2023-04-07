"""adjust user_id length

Revision ID: a1b706c5583a
Revises: 9a1e19f2690c
Create Date: 2023-03-08 16:52:31.272944

"""
import logging

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a1b706c5583a'
down_revision = '9a1e19f2690c'
branch_labels = None
depends_on = None
alembic_logger = logging.getLogger("alembic")


def upgrade():
    alembic_logger.info("Table push_notification_robo Column user_id 100 to 500.")
    op.execute(
        """ALTER TABLE push_notification_robo MODIFY COLUMN user_id VARCHAR(500) NOT NULL COMMENT 'Growin 客戶編號';""")

    alembic_logger.info("Table push_notification_robo Column notification_method 5 to 10.")
    op.execute(
        """ALTER TABLE push_notification_robo MODIFY COLUMN notification_method VARCHAR(10) NOT NULL COMMENT '通知方式
email
line
discord';""")

    alembic_logger.info("Table push_notification_record Column user_id 100 to 500.")
    op.execute(
        """ALTER TABLE push_notification_record MODIFY COLUMN user_id VARCHAR(500) NOT NULL COMMENT 'Growin 客戶編號';""")

    alembic_logger.info("Table push_notification_record Column notification_method 5 to 10.")
    op.execute(
        """ALTER TABLE push_notification_record MODIFY COLUMN notification_method VARCHAR(10) NOT NULL COMMENT '通知方式
email
line
discord';""")


def downgrade():
    alembic_logger.info("Table push_notification_robo Column user_id 500 to 100.")
    op.execute(
        """ALTER TABLE push_notification_robo MODIFY COLUMN user_id VARCHAR(100) NOT NULL COMMENT 'Growin 客戶編號';""")

    alembic_logger.info("Table push_notification_robo Column notification_method 10 to 5.")
#     op.execute(
#         """ALTER TABLE push_notification_robo MODIFY COLUMN notification_method VARCHAR(5) NOT NULL COMMENT '通知方式
# email
# line
# discord';""")

    alembic_logger.info("Table push_notification_record Column user_id 500 to 100.")
    op.execute(
        """ALTER TABLE push_notification_record MODIFY COLUMN user_id VARCHAR(100) NOT NULL COMMENT 'Growin 客戶編號';""")

    alembic_logger.info("Table push_notification_record Column notification_method 10 to 5.")
#     op.execute(
#         """ALTER TABLE push_notification_record MODIFY COLUMN notification_method VARCHAR(5) NOT NULL COMMENT '通知方式
# email
# line
# discord';""")
