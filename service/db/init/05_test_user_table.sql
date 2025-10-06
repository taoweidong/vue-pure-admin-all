/*
Navicat MySQL Data Transfer

Source Server         : 本地MySql
Source Server Version : 80032
Source Host           : localhost:3306
Source Database       : xadmin-fastapi

Target Server Type    : MYSQL
Target Server Version : 80032
File Encoding         : 65001

Date: 2025-10-06 10:00:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for test_user
-- ----------------------------
DROP TABLE IF EXISTS `test_user`;
CREATE TABLE `test_user` (
  `id` char(32) NOT NULL,
  `username` varchar(150) NOT NULL,
  `nickname` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `gender` int NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `creator_id` char(32) DEFAULT NULL,
  `modifier_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `test_user_phone_idx` (`phone`),
  KEY `test_user_email_idx` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;