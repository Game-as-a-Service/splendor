CREATE DATABASE IF NOT EXISTS push_notification;
USE push_notification;
-- -------------------------------------------------------------
-- TablePlus 5.3.0(486)
--
-- https://tableplus.com/
--
-- Database: push_notification
-- Generation Time: 2023-02-24 11:47:54.3230
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `push_notification_record`;
CREATE TABLE `push_notification_record` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
  `user_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'Growin 客戶編號',
  `strategy_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '策略名稱',
  `strategy_category` varchar(4) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '進場 BUY\n出場 SELL',
  `setting_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '設定類型\n自訂 self-robo\n價值機器人 value-robo\n波段機器人 swing-robo\n趨勢機器人 trend-robo',
  `notification_method` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '通知方式\nEmail\nLine',
  `symbols` json NOT NULL DEFAULT (json_array()) COMMENT '追蹤標的列表',
  `details` json NOT NULL DEFAULT (json_object()) COMMENT '策略細節',
  `read_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已讀狀態',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `push_notification_robo`;
CREATE TABLE `push_notification_robo` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
  `user_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'Growin 客戶編號',
  `strategy_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '策略名稱',
  `strategy_category` varchar(4) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '進場 BUY\n出場 SELL',
  `status` varchar(8) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '狀態\n啟用中 active\n停用中 inactive\n刪除 delete',
  `setting_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '設定類型\n自訂 self-robo\n價值機器人 value-robo\n波段機器人 swing-robo\n趨勢機器人 trend-robo',
  `notification_method` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '通知方式\nEmail\nLine',
  `symbols` json NOT NULL DEFAULT (json_array()) COMMENT '追蹤標的列表',
  `details` json NOT NULL DEFAULT (json_object()) COMMENT '策略細節',
  `finished_at` date NOT NULL COMMENT '偵測結束時間',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;