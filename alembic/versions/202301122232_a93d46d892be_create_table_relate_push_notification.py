"""Create Table Relate push_notification

Revision ID: a93d46d892be
Revises: 
Create Date: 2023-01-12 22:32:50.324642

"""
import logging

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a93d46d892be'
down_revision = None
branch_labels = None
depends_on = None
alembic_logger = logging.getLogger("alembic")


def upgrade():
    alembic_logger.info("Create Table push_notification_robo.")
    stm = """
        CREATE TABLE push_notification_robo (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '流水碼',
            user_id VARCHAR(100) NOT NULL COMMENT 'Growin 客戶編號',
            strategy_name VARCHAR(50) NOT NULL COMMENT '策略名稱',
            strategy_category VARCHAR(4) NOT NULL COMMENT '進場 BUY
出場 SELL',
            status VARCHAR(8) NOT NULL COMMENT '狀態
啟用中 active
停用中 inactive
刪除 delete',
            setting_type VARCHAR(10) NOT NULL COMMENT '設定類型
自訂 self-robo
價值機器人 value-robo
波段機器人 swing-robo
趨勢機器人 trend-robo',
            notification_method VARCHAR(5) NOT NULL COMMENT '通知方式
Email
Line',       
            watchlist VARCHAR(100) NOT NULL COMMENT '追蹤清單',
            watchlist_id VARCHAR(32) NOT NULL COMMENT '追蹤清單編號',
            symbols JSON NOT NULL DEFAULT (JSON_ARRAY()) COMMENT '追蹤標的列表',
            details JSON NOT NULL DEFAULT (JSON_OBJECT()) COMMENT '策略細節',
            finished_at DATE NOT NULL COMMENT '偵測結束時間',
            updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP'
        );
    """
    op.execute(stm)

    alembic_logger.info("Create Table push_notification_record.")
    stm = """
        CREATE TABLE push_notification_record (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '流水碼',
            user_id VARCHAR(100) NOT NULL COMMENT 'Growin 客戶編號',
            strategy_name VARCHAR(50) NOT NULL COMMENT '策略名稱',
            strategy_category VARCHAR(4) NOT NULL COMMENT '進場 BUY
出場 SELL',
            setting_type VARCHAR(10) NOT NULL COMMENT '設定類型
自訂 self-robo
價值機器人 value-robo
波段機器人 swing-robo
趨勢機器人 trend-robo',
            notification_method VARCHAR(5) NOT NULL COMMENT '通知方式
Email
Line',       
            watchlist VARCHAR(100) NOT NULL COMMENT '追蹤清單',
            watchlist_id VARCHAR(32) NOT NULL COMMENT '追蹤清單編號',
            symbols JSON NOT NULL DEFAULT (JSON_ARRAY()) COMMENT '追蹤標的列表',
            details JSON NOT NULL DEFAULT (JSON_OBJECT()) COMMENT '策略細節',
            read_status BOOLEAN NOT NULL DEFAULT 0 COMMENT '已讀狀態',
            updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP'
        );
    """
    op.execute(stm)


def downgrade():
    alembic_logger.info("Drop Table push_notification_robo;")
    op.execute("""DROP TABLE push_notification_robo;""")
    alembic_logger.info("Drop Table push_notification_record;")
    op.execute("""DROP TABLE push_notification_record;""")
