CREATE DATABASE IF NOT EXISTS user_profile;

USE user_profile;

-- -------------------------------------------------------------

-- TablePlus 5.3.0(486)

--

-- https://tableplus.com/

--

-- Database: user_profile

-- Generation Time: 2023-03-02 16:21:38.6480

-- -------------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */

;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */

;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */

;

/*!40101 SET NAMES utf8mb4 */

;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */

;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */

;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */

;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */

;

DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE
    `alembic_version` (
        `version_num` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
        PRIMARY KEY (`version_num`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3 COLLATE = utf8_unicode_ci;

DROP TABLE IF EXISTS `business_account`;

CREATE TABLE
    `business_account` (
        `user_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '企業帳號',
        `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '密碼',
        `company` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT '企業名稱',
        `company_code` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT '企業代號',
        `status` tinyint(1) NOT NULL COMMENT '狀態\nTrue: 可使用,\nFalse: 不可使用',
        `plan` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '方案\nBasic Monthly: 基本方案（月繳）,\nBasic Yearly: 基本方案（年繳）,\nPremium Monthly: 進階方案（月繳）,\nPremium Yearly: 進階方案（年繳）',
        `subscribed_at` date DEFAULT NULL COMMENT '訂閱日期',
        `expire_at` date DEFAULT NULL COMMENT '到期日期',
        `watchlist_index` tinyint DEFAULT '0' COMMENT '上次瀏覽的追蹤清單 index',
        `watchlist` json NOT NULL COMMENT '觀察清單',
        `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
        `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
        PRIMARY KEY (`user_id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3 COLLATE = utf8_unicode_ci;

DROP TABLE IF EXISTS `cancel_subscribe_record`;

CREATE TABLE
    `cancel_subscribe_record` (
        `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
        `subscription_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '訂閱編號',
        `customer_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Stripe 客戶編號',
        `canceled_at` datetime DEFAULT NULL COMMENT '提出取消時間',
        `expire_at` datetime DEFAULT NULL COMMENT '到期時間',
        `reason` json DEFAULT NULL COMMENT '原因',
        `recovered_at` datetime DEFAULT NULL COMMENT '恢復訂閱時間',
        `status` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT '狀態, canceled: 取消訂閱, recovered: 恢復訂閱',
        `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
        `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3 COLLATE = utf8_unicode_ci;

DROP TABLE IF EXISTS `institution_exclusive_offers`;

CREATE TABLE
    `institution_exclusive_offers` (
        `id` int NOT NULL AUTO_INCREMENT COMMENT '流水碼',
        `user_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Growin 使用者編號',
        `institution` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT '機構名稱',
        `collaborate` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT '合作案',
        `package` json NOT NULL COMMENT '優惠內容\nminimumOrder: 低消\ncharge: 手續費',
        `start_at` datetime NOT NULL COMMENT '優惠開始時間',
        `end_at` datetime DEFAULT NULL COMMENT '優惠結束時間',
        `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
        `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3 COLLATE = utf8_unicode_ci;

DROP TABLE IF EXISTS `nike_customer_info`;

CREATE TABLE
    `nike_customer_info` (
        `user_id` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Growin 客戶編號',
        `customer_id` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'stripe 客戶編號',
        `name` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '姓名',
        `phone` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '手機號碼',
        `email` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '電子郵件',
        `plan` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT '方案\nFree: 免費方案,\nBasic Yearly: 基本方案（年繳）,\nBasic Monthly: 基本方案（月繳）,\nPremium Yearly：進階方案（年繳）,\nPremium Monthly: 進階方案（月繳）',
        `subscribed_at` date DEFAULT NULL COMMENT '訂閱日期',
        `expire_at` date DEFAULT NULL COMMENT '到期日期',
        `status` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Stripe 客戶訂閱狀態\ninactive: 待用,\ntrialing: 適用期,\nactive: 正式使用,\ncanceled: 已取消',
        `watchlist_index` tinyint DEFAULT '0' COMMENT '上次瀏覽的追蹤清單 index',
        `watchlist` json NOT NULL COMMENT '觀察清單',
        `use_tag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '使用服務',
        `line_user_id` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'LINE 使用者編號',
        `line_nonce` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'LINE NONCE',
        `line_bind_status` tinyint(1) DEFAULT '0' COMMENT 'LINE 綁定狀態',
        `line_bind_at` datetime DEFAULT NULL COMMENT 'LINE 綁定時間',
        `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '資料異動時間，當update資料時自動更新 CURRENT_TIMESTAMP',
        `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '資料建立時間，當資料建立時自動設為 CURRENT_TIMESTAMP',
        PRIMARY KEY (`user_id`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3 COLLATE = utf8_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */

;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */

;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */

;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */

;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */

;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */

;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */

;