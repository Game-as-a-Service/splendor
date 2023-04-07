CREATE DATABASE IF NOT EXISTS tradingvalley_manager;
USE tradingvalley_manager;
-- -------------------------------------------------------------
-- TablePlus 5.3.0(486)
--
-- https://tableplus.com/
--
-- Database: tradingvalley_manager
-- Generation Time: 2023-02-24 22:08:25.4120
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
  `version_num` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `db_connection_info`;
CREATE TABLE `db_connection_info` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
  `project` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'project name',
  `project_branch` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'project branch',
  `DB_username` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'DB username',
  `DB_password` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'DB password',
  `DB_host` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'DB host',
  `DB_name` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'DB name',
  `DB_port` int NOT NULL COMMENT 'DB port',
  `DB_permission` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT 'DB permission : create, read, update, delete, all',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `db_connection_log`;
CREATE TABLE `db_connection_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
  `project` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'project name',
  `project_branch` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'project branch',
  `ip` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'ip address',
  `status` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'status : success, fail',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `pwd_info`;
CREATE TABLE `pwd_info` (
  `user_id` varchar(15) COLLATE utf8_unicode_ci NOT NULL COMMENT '流水號由註冊時間組成',
  `account_hash` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT '帳號（公司 email 採用 sha256）',
  `password_hash` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT '密碼（密碼採用 sha256）',
  `fail_counts` int NOT NULL COMMENT '登入失敗次數（預設為 0）',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `user_id` varchar(15) COLLATE utf8_unicode_ci NOT NULL COMMENT '流水號由註冊時間組成',
  `username` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '使用者名稱 由英文姓名組成',
  `chinese_name` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT '中文姓名',
  `email` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT 'email',
  `job_title` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT '職稱 Boss, Product manager, UI designer, Frontend Engineer, Backend Engineer, Quantitative Engineer, Marketing',
  `status` int NOT NULL COMMENT '狀態 0: 正常 1: 凍結 2: 等待刪除 3: 等待開通 4: 忘記密碼（預設為 3 等待開通)',
  `opening_state` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT '帳號可登入的狀態（預設為 normal）normal: 一般使用者 all: 全天使用者',
  `opening_hours` varchar(5) COLLATE utf8_unicode_ci NOT NULL COMMENT '帳號每日（預設為 07-24）開放時間 07-24: 台灣時間早上七點至 晚上24點 00-00: 全天開放使用',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `user_sign_in_log`;
CREATE TABLE `user_sign_in_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '流水號',
  `user_id` varchar(15) COLLATE utf8_unicode_ci NOT NULL COMMENT 'user id註冊時間組成',
  `sign_in_at` datetime NOT NULL COMMENT '登入時間',
  `ip_address` varchar(39) COLLATE utf8_unicode_ci NOT NULL COMMENT '登入ip 位址 儲存 IPv4 為主 IPv4: 15 字符 IPv6: 39 字符',
  `status` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT '登入狀態 Success 成功 Wrong-password 密碼錯誤 Blocked 凍結-密碼錯誤超過 3 次 Unscheduled-login 非規定時間登入',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `video_info`;
CREATE TABLE `video_info` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
  `category` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '類別\nmarket-analysis: 市場分析,\noriented-analysis: 五力分析,\nfinance-knowledge: 金融知識',
  `title` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '標題',
  `content` varchar(10000) COLLATE utf8_unicode_ci NOT NULL COMMENT '內文',
  `symbol` json NOT NULL COMMENT '標的列表',
  `published_at` date NOT NULL COMMENT '影音發佈時間',
  `photo_url` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT '封面照 URL',
  `video_url` varchar(500) COLLATE utf8_unicode_ci NOT NULL COMMENT '影音 URL',
  `status` tinyint(1) NOT NULL COMMENT '開放狀態',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;