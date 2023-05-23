"""create noble_info table

Revision ID: 923ab765a125
Revises: c688d28a6fe3
Create Date: 2023-05-15 17:51:15.737793

"""
from alembic import op
import logging


# revision identifiers, used by Alembic.
revision = '923ab765a125'
down_revision = 'c688d28a6fe3'
branch_labels = None
depends_on = None
alembic_logger = logging.getLogger('alembic')


def upgrade():
    alembic_logger.info("Create Table noble_info.\n")
    stm = """
        CREATE TABLE noble_info (
            noble_id int NOT NULL COMMENT '貴族卡編號',
            score int NOT NULL COMMENT '分數',
            diamond int NOT NULL COMMENT '鑽石',
            sapphire int NOT NULL COMMENT '藍寶石',
            emerald int NOT NULL COMMENT '綠寶石',
            ruby int NOT NULL COMMENT '紅寶石',
            onyx int NOT NULL COMMENT '瑪瑙',
            PRIMARY KEY (noble_id));
    """
    op.execute(stm)
    alembic_logger.info("Insert into noble_info.\n")
    stm = """
        INSERT INTO noble_info VALUES(1, 3,3,0,0,3,3),
                    (2, 3,0,0,0,4,4),
                    (3, 3,4,0,0,0,4),
                    (4, 3,4,4,0,0,0),
                    (5, 3,0,4,4,0,0),
                    (6, 3,0,3,3,3,0),
                    (7, 3,0,0,3,3,3),
                    (8, 3,3,3,0,0,3),
                    (9, 3,0,0,4,4,0),
                    (10,3,3,3,3,0,0);
                    
    """
    op.execute(stm)

    alembic_logger.info("Create Table development_card_info.\n")
    stm = """
        CREATE TABLE development_card_info (
            level int NOT NULL COMMENT 'level',
            id int NOT NULL COMMENT 'id',
            score int NOT NULL COMMENT '分數',
            diamond int NOT NULL COMMENT '鑽石',
            sapphire int NOT NULL COMMENT '藍寶石',
            emerald int NOT NULL COMMENT '綠寶石',
            ruby int NOT NULL COMMENT '紅寶石',
            onyx int NOT NULL COMMENT '瑪瑙',
            bonus varchar(20) NOT NULL COMMENT '獲得寶石',
            PRIMARY KEY (level,id));
    """
    op.execute(stm)

    alembic_logger.info("Insert into development_card_info.\n")
    stm = """
        INSERT INTO development_card_info VALUES
                    (1, 1, 0, 1, 1, 1, 0, 1,'ruby'),
                    (1, 2, 0, 1, 1, 0, 1, 1,'emerald'),
                    (1, 3, 0, 0, 2, 0, 2, 0,'emerald'),
                    (1, 4, 0, 1, 0, 1, 2, 1,'sapphire'),
                    (1, 5, 0, 0, 0, 2, 1, 0,'onyx'),
                    (1, 6, 0, 0, 0, 0, 3, 0,'emerald'),
                    (1, 7, 0, 2, 2, 0, 1, 0,'onyx'),
                    (1, 8, 0, 1, 0, 2, 2, 0,'sapphire'),
                    (1, 9, 0, 0, 0, 1, 3, 1,'onyx'),
                    (1, 10, 1, 0, 0, 0, 0, 4,'emerald'),
                    (1, 11, 0, 1, 1, 0, 1, 2,'emerald'),
                    (1, 12, 0, 2, 0, 1, 0, 2,'ruby'),
                    (1, 13, 0, 3, 0, 0, 0, 0,'ruby'),
                    (1, 14, 0, 1, 0, 0, 0, 2,'sapphire'),
                    (1, 15, 0, 0, 2, 1, 0, 0,'ruby'),
                    (1, 16, 0, 0, 2, 0, 0, 2,'diamond'),
                    (1, 17, 0, 0, 2, 3, 1, 0,'sapphire'),
                    (1, 18, 0, 0, 3, 0, 0, 0,'diamond'),
                    (1, 19, 0, 3, 1, 0, 0, 1,'diamond'),
                    (1, 20, 0, 0, 2, 2, 0, 1,'diamond'),
                    (1, 21, 0, 1, 3, 1, 0, 0,'emerald'),
                    (1, 22, 0, 0, 0, 0, 2, 1,'diamond'),
                    (1, 23, 0, 0, 1, 2, 1, 1,'diamond'),
                    (1, 24, 0, 1, 2, 1, 1, 0,'onyx'),
                    (1, 25, 0, 0, 0, 3, 0, 0,'onyx'),
                    (1, 26, 0, 2, 1, 1, 0, 1,'ruby'),
                    (1, 27, 0, 0, 0, 2, 0, 2,'sapphire'),
                    (1, 28, 0, 1, 0, 1, 1, 1,'sapphire'),
                    (1, 29, 1, 0, 0, 0, 4, 0,'sapphire'),
                    (1, 30, 0, 2, 0, 0, 2, 0,'ruby'),
                    (1, 31, 0, 1, 0, 0, 1, 3,'ruby'),
                    (1, 32, 1, 0, 0, 4, 0, 0,'diamond'),
                    (1, 33, 0, 0, 1, 1, 1, 1,'diamond'),
                    (1, 34, 1, 0, 4, 0, 0, 0,'onyx'),
                    (1, 35, 0, 2, 0, 2, 0, 0,'onyx'),
                    (1, 36, 0, 1, 1, 1, 1, 0,'onyx'),
                    (1, 37, 0, 0, 0, 0, 0, 3,'onyx'),
                    (1, 38, 0, 2, 1, 0, 0, 0,'emerald'),
                    (1, 39, 0, 0, 1, 0, 2, 2,'emerald'),
                    (1, 40, 1, 4, 0, 0, 0, 0,'ruby'),
                    (2, 1, 1, 3, 2, 2, 0, 0,'onyx'),
                    (2, 2, 3, 0, 6, 0, 0, 0,'sapphire'),
                    (2, 3, 1, 0, 2, 2, 3, 0,'sapphire'),
                    (2, 4, 2, 0, 0, 0, 5, 3,'diamond'),
                    (2, 5, 2, 0, 5, 3, 0, 0,'emerald'),
                    (2, 6, 1, 0, 0, 3, 2, 2,'diamond'),
                    (2, 7, 1, 2, 3, 0, 3, 0,'diamond'),
                    (2, 8, 2, 0, 5, 0, 0, 0,'sapphire'),
                    (2, 9, 2, 0, 0, 0, 5, 0,'diamond'),
                    (2, 10, 2, 0, 0, 5, 0, 0,'emerald'),
                    (2, 11, 3, 0, 0, 6, 0, 0,'emerald'),
                    (2, 12, 3, 6, 0, 0, 0, 0,'diamond'),
                    (2, 13, 2, 0, 0, 1, 4, 2,'diamond'),
                    (2, 14, 3, 0, 0, 0, 0, 6,'onyx'),
                    (2, 15, 2, 4, 2, 0, 0, 1,'emerald'),
                    (2, 16, 3, 0, 0, 0, 6, 0,'ruby'),
                    (2, 17, 2, 5, 3, 0, 0, 0,'sapphire'),
                    (2, 18, 1, 2, 3, 0, 0, 2,'emerald'),
                    (2, 19, 2, 1, 4, 2, 0, 0,'ruby'),
                    (2, 20, 1, 2, 3, 0, 2, 0,'ruby'),
                    (2, 21, 2, 0, 0, 5, 3, 0,'onyx'),
                    (2, 22, 1, 0, 3, 0, 2, 3,'ruby'),
                    (2, 23, 1, 0, 2, 3, 0, 3,'sapphire'),
                    (2, 24, 1, 3, 0, 2, 3, 0,'emerald'),
                    (2, 25, 1, 3, 0, 3, 0, 2,'onyx'),
                    (2, 26, 2, 0, 0, 0, 0, 5,'ruby'),
                    (2, 27, 2, 3, 0, 0, 0, 5,'ruby'),
                    (2, 28, 2, 5, 0, 0, 0, 0,'onyx'),
                    (2, 29, 2, 2, 0, 0, 1, 4,'sapphire'),
                    (2, 30, 0, 2, 0, 0, 2, 0,'ruby'),
                    (3, 1, 5, 0, 0, 0, 7, 3,'onyx'),
                    (3, 2, 4, 0, 0, 3, 6, 3,'onyx'),
                    (3, 3, 4, 3, 6, 3, 0, 0,'emerald'),
                    (3, 4, 4, 0, 0, 0, 0, 7,'diamond'),
                    (3, 5, 5, 0, 7, 3, 0, 0,'emerald'),
                    (3, 6, 4, 6, 3, 0, 0, 3,'sapphire'),
                    (3, 7, 3, 5, 3, 0, 3, 3,'emerald'),
                    (3, 8, 4, 0, 0, 0, 7, 0,'onyx'),
                    (3, 9, 4, 0, 3, 6, 3, 0,'ruby'),
                    (3, 10, 3, 3, 0, 3, 3, 5,'sapphire'),
                    (3, 11, 3, 3, 5, 3, 0, 3,'ruby'),
                    (3, 12, 3, 0, 3, 3, 5, 3,'diamond'),
                    (3, 13, 3, 3, 3, 5, 3, 0,'onyx'),
                    (3, 14, 4, 0, 7, 0, 0, 0,'emerald'),
                    (3, 15, 5, 0, 0, 7, 3, 0,'ruby'),
                    (3, 16, 4, 7, 0, 0, 0, 0,'sapphire'),
                    (3, 17, 4, 0, 0, 7, 0, 0,'ruby'),
                    (3, 18, 5, 3, 0, 0, 0, 7,'diamond'),
                    (3, 19, 4, 3, 0, 0, 3, 6,'diamond'),
                    (3, 20, 5, 7, 3, 0, 0, 0,'sapphire')
                    
    """
    op.execute(stm)

    alembic_logger.info("Create Table game_info.\n")
    stm = """
        CREATE TABLE game_info (
            game_id varchar(36) NOT NULL COMMENT '遊戲編號',
            status varchar(10) NOT NULL COMMENT '遊戲狀態(processing,lastRound,end)',
            turn varchar(36) NOT NULL COMMENT '輪到誰',
            whos_winner varchar(36) COMMENT '勝利玩家',
            PRIMARY KEY (game_id));
    """
    op.execute(stm)

    alembic_logger.info("Create Table player_info.\n")
    stm = """
        CREATE TABLE player_info (
            game_id varchar(36) NOT NULL COMMENT '遊戲編號',
            player_id varchar(36) NOT NULL COMMENT '玩家編號',   
            seq int NOT NULL  COMMENT '順序',   
            score int NOT NULL COMMENT '分數',
            diamond int NOT NULL COMMENT '鑽石',
            sapphire int NOT NULL COMMENT '藍寶石',
            emerald int NOT NULL COMMENT '綠寶石',
            ruby int NOT NULL COMMENT '紅寶石',
            onyx int NOT NULL COMMENT '瑪瑙',
            gold int NOT NULL COMMENT '黃金',
            bonus_diamond int NOT NULL COMMENT '永久鑽石',
            bonus_sapphire int NOT NULL COMMENT '永久藍寶石',
            bonus_emerald int NOT NULL COMMENT '永久綠寶石',
            bonus_ruby int NOT NULL COMMENT '永久紅寶石',
            bonus_onyx int NOT NULL COMMENT '永久瑪瑙',
            PRIMARY KEY (game_id,player_id));
    """
    op.execute(stm)

    alembic_logger.info("Create Table table_info.\n")
    stm = """
        CREATE TABLE table_info (
            game_id varchar(36) NOT NULL COMMENT '遊戲編號',
            table_id varchar(36) NOT NULL COMMENT '桌面編號',  
            diamond int NOT NULL COMMENT '鑽石',
            sapphire int NOT NULL COMMENT '藍寶石',
            emerald int NOT NULL COMMENT '綠寶石',
            ruby int NOT NULL COMMENT '紅寶石',
            onyx int NOT NULL COMMENT '瑪瑙',
            gold int NOT NULL COMMENT '黃金',
            PRIMARY KEY (game_id,table_id));
    """
    op.execute(stm)

    alembic_logger.info("Create Table table_nobles_info.\n")
    stm = """
        CREATE TABLE table_nobles_info (
            game_id varchar(36) NOT NULL COMMENT '遊戲編號',
            table_id varchar(36) NOT NULL COMMENT '桌面編號',
            noble_id int NOT NULL COMMENT '貴族卡編號',
            seq int NOT NULL COMMENT '順序',            
            PRIMARY KEY (game_id,table_id,noble_id));
    """
    op.execute(stm)

    alembic_logger.info("Create Table table_development_card_info.\n")
    stm = """
        CREATE TABLE table_development_card_info (
            game_id varchar(36) NOT NULL COMMENT '遊戲編號',
            table_id varchar(36) NOT NULL COMMENT '桌面編號',
            level int NOT NULL COMMENT 'level',
            id int NOT NULL COMMENT '編號',
            seq int NOT NULL COMMENT '順序',   
            status varchar(10)  NOT NULL COMMENT '狀態(indeck,ontable)',   
            PRIMARY KEY (game_id,table_id,level,id));
    """
    op.execute(stm)

    alembic_logger.info("Create Table player_noble_info.\n")
    stm = """
        CREATE TABLE player_noble_info (
            game_id varchar(36) NOT NULL COMMENT '遊戲編號',
            player_id varchar(36) NOT NULL COMMENT '玩家編號',            
            noble_id int NOT NULL COMMENT '貴族卡編號',     
            PRIMARY KEY (game_id,player_id,noble_id));
    """
    op.execute(stm)

    alembic_logger.info("Create Table player_development_card_info.\n")
    stm = """
        CREATE TABLE player_development_card_info (
            game_id varchar(36)  NOT NULL COMMENT '遊戲編號',
            player_id varchar(36)  NOT NULL COMMENT '玩家編號',            
            level int NOT NULL COMMENT 'level',
            id int NOT NULL COMMENT '編號', 
            status varchar(10) NOT NULL COMMENT '狀態(buy,reserve)', 
            PRIMARY KEY (game_id,player_id,level,id));
    """
    op.execute(stm)


def downgrade():
    alembic_logger.info("Drop Table noble_info;")
    op.execute("""DROP TABLE noble_info;""")

    alembic_logger.info("Drop Table development_card_info;")
    op.execute("""DROP TABLE development_card_info;""")

    alembic_logger.info("Drop Table game_info;")
    op.execute("""DROP TABLE game_info;""")

    alembic_logger.info("Drop Table player_info;")
    op.execute("""DROP TABLE player_info;""")

    alembic_logger.info("Drop Table table_info;")
    op.execute("""DROP TABLE table_info;""")

    alembic_logger.info("Drop Table table_nobles_info;")
    op.execute("""DROP TABLE table_nobles_info;""")

    alembic_logger.info("Drop Table table_development_card_info;")
    op.execute("""DROP TABLE table_development_card_info;""")

    alembic_logger.info("Drop Table player_noble_info;")
    op.execute("""DROP TABLE player_noble_info;""")

    alembic_logger.info("Drop Table player_development_card_info;")
    op.execute("""DROP TABLE player_development_card_info;""")
