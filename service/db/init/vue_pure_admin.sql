/*
Navicat MySQL Data Transfer

Source Server         : 本地MySql
Source Server Version : 80032
Source Host           : localhost:3306
Source Database       : xadmin-fastapi

Target Server Type    : MYSQL
Target Server Version : 80032
File Encoding         : 65001

Date: 2025-10-04 08:05:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for settings_setting
-- ----------------------------
DROP TABLE IF EXISTS `settings_setting`;
CREATE TABLE `settings_setting` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `name` varchar(128) NOT NULL,
  `value` longtext,
  `category` varchar(128) NOT NULL,
  `encrypted` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `settings_setting_creator_id_03dbca4f_fk_system_userinfo_id` (`creator_id`),
  KEY `settings_setting_dept_belong_id_09c1ecb2_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `settings_setting_modifier_id_f14779f7_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `settings_setting_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `settings_setting_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `settings_setting_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_datapermission
-- ----------------------------
DROP TABLE IF EXISTS `system_datapermission`;
CREATE TABLE `system_datapermission` (
  `mode_type` smallint NOT NULL,
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `rules` json NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `system_datapermissio_dept_belong_id_75b396d3_fk_system_de` (`dept_belong_id`),
  KEY `system_datapermission_creator_id_5800c16f_fk_system_userinfo_id` (`creator_id`),
  KEY `system_datapermission_modifier_id_85b8640c_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_datapermission_ibfk_1` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_datapermission_ibfk_2` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_datapermission_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_datapermission_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_datapermission_menu`;
CREATE TABLE `system_datapermission_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `datapermission_id` char(32) NOT NULL,
  `menu_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_datapermission_me_datapermission_id_menu_i_7df1cef0_uniq` (`datapermission_id`,`menu_id`),
  KEY `system_datapermission_menu_menu_id_b8165507_fk_system_menu_id` (`menu_id`),
  CONSTRAINT `system_datapermission_menu_ibfk_1` FOREIGN KEY (`datapermission_id`) REFERENCES `system_datapermission` (`id`),
  CONSTRAINT `system_datapermission_menu_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_deptinfo
-- ----------------------------
DROP TABLE IF EXISTS `system_deptinfo`;
CREATE TABLE `system_deptinfo` (
  `mode_type` smallint NOT NULL,
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `name` varchar(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `rank` int NOT NULL,
  `auto_bind` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `parent_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `system_deptinfo_creator_id_6304526c_fk_system_userinfo_id` (`creator_id`),
  KEY `system_deptinfo_dept_belong_id_40eea2f6_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_deptinfo_modifier_id_eadcba8a_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_deptinfo_parent_id_86e73520_fk_system_deptinfo_id` (`parent_id`),
  CONSTRAINT `system_deptinfo_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_deptinfo_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_deptinfo_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_deptinfo_ibfk_4` FOREIGN KEY (`parent_id`) REFERENCES `system_deptinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_deptinfo_roles
-- ----------------------------
DROP TABLE IF EXISTS `system_deptinfo_roles`;
CREATE TABLE `system_deptinfo_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `deptinfo_id` char(32) NOT NULL,
  `userrole_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_deptinfo_roles_deptinfo_id_userrole_id_f390140f_uniq` (`deptinfo_id`,`userrole_id`),
  KEY `system_deptinfo_roles_userrole_id_353c349d_fk_system_userrole_id` (`userrole_id`),
  CONSTRAINT `system_deptinfo_roles_ibfk_1` FOREIGN KEY (`deptinfo_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_deptinfo_roles_ibfk_2` FOREIGN KEY (`userrole_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_deptinfo_rules
-- ----------------------------
DROP TABLE IF EXISTS `system_deptinfo_rules`;
CREATE TABLE `system_deptinfo_rules` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `deptinfo_id` char(32) NOT NULL,
  `datapermission_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_deptinfo_rules_deptinfo_id_datapermissi_d486df17_uniq` (`deptinfo_id`,`datapermission_id`),
  KEY `system_deptinfo_rule_datapermission_id_204684d2_fk_system_da` (`datapermission_id`),
  CONSTRAINT `system_deptinfo_rules_ibfk_1` FOREIGN KEY (`datapermission_id`) REFERENCES `system_datapermission` (`id`),
  CONSTRAINT `system_deptinfo_rules_ibfk_2` FOREIGN KEY (`deptinfo_id`) REFERENCES `system_deptinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_fieldpermission
-- ----------------------------
DROP TABLE IF EXISTS `system_fieldpermission`;
CREATE TABLE `system_fieldpermission` (
  `id` varchar(128) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `menu_id` char(32) NOT NULL,
  `role_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_fieldpermission_role_id_menu_id_c48f40b4_uniq` (`role_id`,`menu_id`),
  KEY `system_fieldpermission_creator_id_9d8ac4c5_fk_system_userinfo_id` (`creator_id`),
  KEY `system_fieldpermissi_dept_belong_id_d87dc16b_fk_system_de` (`dept_belong_id`),
  KEY `system_fieldpermissi_modifier_id_7e9365a0_fk_system_us` (`modifier_id`),
  KEY `system_fieldpermission_menu_id_5611ae83_fk_system_menu_id` (`menu_id`),
  CONSTRAINT `system_fieldpermission_ibfk_1` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_fieldpermission_ibfk_2` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_fieldpermission_ibfk_3` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_fieldpermission_ibfk_4` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`),
  CONSTRAINT `system_fieldpermission_ibfk_5` FOREIGN KEY (`role_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_fieldpermission_field
-- ----------------------------
DROP TABLE IF EXISTS `system_fieldpermission_field`;
CREATE TABLE `system_fieldpermission_field` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fieldpermission_id` varchar(128) NOT NULL,
  `modellabelfield_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_fieldpermission_f_fieldpermission_id_model_0f9f3e82_uniq` (`fieldpermission_id`,`modellabelfield_id`),
  KEY `system_fieldpermissi_modellabelfield_id_3aa9e0aa_fk_system_mo` (`modellabelfield_id`),
  CONSTRAINT `system_fieldpermission_field_ibfk_1` FOREIGN KEY (`fieldpermission_id`) REFERENCES `system_fieldpermission` (`id`),
  CONSTRAINT `system_fieldpermission_field_ibfk_2` FOREIGN KEY (`modellabelfield_id`) REFERENCES `system_modellabelfield` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `menu_type` smallint NOT NULL,
  `name` varchar(128) NOT NULL,
  `rank` int NOT NULL,
  `path` varchar(255) NOT NULL,
  `component` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `method` varchar(10) DEFAULT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `parent_id` char(32) DEFAULT NULL,
  `meta_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `meta_id` (`meta_id`),
  KEY `system_menu_creator_id_d58495af_fk_system_userinfo_id` (`creator_id`),
  KEY `system_menu_dept_belong_id_ed403c1c_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_menu_modifier_id_49b4db71_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_menu_parent_id_c715739f_fk_system_menu_id` (`parent_id`),
  CONSTRAINT `system_menu_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_menu_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_menu_ibfk_3` FOREIGN KEY (`meta_id`) REFERENCES `system_menumeta` (`id`),
  CONSTRAINT `system_menu_ibfk_4` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_menu_ibfk_5` FOREIGN KEY (`parent_id`) REFERENCES `system_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_menumeta
-- ----------------------------
DROP TABLE IF EXISTS `system_menumeta`;
CREATE TABLE `system_menumeta` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `r_svg_name` varchar(255) DEFAULT NULL,
  `is_show_menu` tinyint(1) NOT NULL,
  `is_show_parent` tinyint(1) NOT NULL,
  `is_keepalive` tinyint(1) NOT NULL,
  `frame_url` varchar(255) DEFAULT NULL,
  `frame_loading` tinyint(1) NOT NULL,
  `transition_enter` varchar(255) DEFAULT NULL,
  `transition_leave` varchar(255) DEFAULT NULL,
  `is_hidden_tag` tinyint(1) NOT NULL,
  `fixed_tag` tinyint(1) NOT NULL,
  `dynamic_level` int NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_menumeta_creator_id_02956d64_fk_system_userinfo_id` (`creator_id`),
  KEY `system_menumeta_dept_belong_id_e65ac812_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_menumeta_modifier_id_7bc4d182_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_menumeta_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_menumeta_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_menumeta_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_menu_model
-- ----------------------------
DROP TABLE IF EXISTS `system_menu_model`;
CREATE TABLE `system_menu_model` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` char(32) NOT NULL,
  `modellabelfield_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_menu_model_menu_id_modellabelfield_id_20bd2666_uniq` (`menu_id`,`modellabelfield_id`),
  KEY `system_menu_model_modellabelfield_id_33aabef8_fk_system_mo` (`modellabelfield_id`),
  CONSTRAINT `system_menu_model_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`),
  CONSTRAINT `system_menu_model_ibfk_2` FOREIGN KEY (`modellabelfield_id`) REFERENCES `system_modellabelfield` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_modellabelfield
-- ----------------------------
DROP TABLE IF EXISTS `system_modellabelfield`;
CREATE TABLE `system_modellabelfield` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `field_type` smallint NOT NULL,
  `name` varchar(128) NOT NULL,
  `label` varchar(128) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `parent_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_modellabelfield_name_parent_id_f1e3af72_uniq` (`name`,`parent_id`),
  KEY `system_modellabelfield_creator_id_69e9dc08_fk_system_userinfo_id` (`creator_id`),
  KEY `system_modellabelfie_dept_belong_id_c80332c5_fk_system_de` (`dept_belong_id`),
  KEY `system_modellabelfie_modifier_id_27595fd8_fk_system_us` (`modifier_id`),
  KEY `system_modellabelfie_parent_id_9988459e_fk_system_mo` (`parent_id`),
  CONSTRAINT `system_modellabelfield_ibfk_1` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_modellabelfield_ibfk_2` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_modellabelfield_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `system_modellabelfield` (`id`),
  CONSTRAINT `system_modellabelfield_ibfk_4` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_noticemessage
-- ----------------------------
DROP TABLE IF EXISTS `system_noticemessage`;
CREATE TABLE `system_noticemessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `level` varchar(20) NOT NULL,
  `notice_type` smallint NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` longtext,
  `extra_json` json DEFAULT NULL,
  `publish` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_noticemessage_creator_id_f4ba0a1c_fk_system_userinfo_id` (`creator_id`),
  KEY `system_noticemessage_dept_belong_id_c0ca570e_fk_system_de` (`dept_belong_id`),
  KEY `system_noticemessage_modifier_id_2d93e397_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_noticemessage_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_noticemessage_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_noticemessage_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_noticemessage_file
-- ----------------------------
DROP TABLE IF EXISTS `system_noticemessage_file`;
CREATE TABLE `system_noticemessage_file` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `noticemessage_id` bigint NOT NULL,
  `uploadfile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_noticemessage_fil_noticemessage_id_uploadf_dc757fde_uniq` (`noticemessage_id`,`uploadfile_id`),
  KEY `system_noticemessage_uploadfile_id_0147bce2_fk_system_up` (`uploadfile_id`),
  CONSTRAINT `system_noticemessage_file_ibfk_1` FOREIGN KEY (`noticemessage_id`) REFERENCES `system_noticemessage` (`id`),
  CONSTRAINT `system_noticemessage_file_ibfk_2` FOREIGN KEY (`uploadfile_id`) REFERENCES `system_uploadfile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_noticemessage_notice_dept
-- ----------------------------
DROP TABLE IF EXISTS `system_noticemessage_notice_dept`;
CREATE TABLE `system_noticemessage_notice_dept` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `noticemessage_id` bigint NOT NULL,
  `deptinfo_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_noticemessage_not_noticemessage_id_deptinf_b31ae2db_uniq` (`noticemessage_id`,`deptinfo_id`),
  KEY `system_noticemessage_deptinfo_id_a28c5bd4_fk_system_de` (`deptinfo_id`),
  CONSTRAINT `system_noticemessage_notice_dept_ibfk_1` FOREIGN KEY (`deptinfo_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_noticemessage_notice_dept_ibfk_2` FOREIGN KEY (`noticemessage_id`) REFERENCES `system_noticemessage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_noticemessage_notice_role
-- ----------------------------
DROP TABLE IF EXISTS `system_noticemessage_notice_role`;
CREATE TABLE `system_noticemessage_notice_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `noticemessage_id` bigint NOT NULL,
  `userrole_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_noticemessage_not_noticemessage_id_userrol_4326557a_uniq` (`noticemessage_id`,`userrole_id`),
  KEY `system_noticemessage_userrole_id_68bccfc7_fk_system_us` (`userrole_id`),
  CONSTRAINT `system_noticemessage_notice_role_ibfk_1` FOREIGN KEY (`noticemessage_id`) REFERENCES `system_noticemessage` (`id`),
  CONSTRAINT `system_noticemessage_notice_role_ibfk_2` FOREIGN KEY (`userrole_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_noticeuserread
-- ----------------------------
DROP TABLE IF EXISTS `system_noticeuserread`;
CREATE TABLE `system_noticeuserread` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `unread` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `notice_id` bigint NOT NULL,
  `owner_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_noticeuserread_owner_id_notice_id_3152c150_uniq` (`owner_id`,`notice_id`),
  KEY `system_noti_owner_i_63a25a_idx` (`owner_id`,`unread`),
  KEY `system_noticeuserread_creator_id_b8efc60a_fk_system_userinfo_id` (`creator_id`),
  KEY `system_noticeuserrea_dept_belong_id_81269613_fk_system_de` (`dept_belong_id`),
  KEY `system_noticeuserread_modifier_id_a50a55f3_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_noticeuserrea_notice_id_ae4170d6_fk_system_no` (`notice_id`),
  KEY `system_noticeuserread_unread_ca59b7a4` (`unread`),
  CONSTRAINT `system_noticeuserread_ibfk_1` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_noticeuserread_ibfk_2` FOREIGN KEY (`notice_id`) REFERENCES `system_noticemessage` (`id`),
  CONSTRAINT `system_noticeuserread_ibfk_3` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_noticeuserread_ibfk_4` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_noticeuserread_ibfk_5` FOREIGN KEY (`owner_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_operationlog
-- ----------------------------
DROP TABLE IF EXISTS `system_operationlog`;
CREATE TABLE `system_operationlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `module` varchar(64) DEFAULT NULL,
  `path` varchar(400) DEFAULT NULL,
  `body` longtext,
  `method` varchar(8) DEFAULT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `browser` varchar(64) DEFAULT NULL,
  `system` varchar(64) DEFAULT NULL,
  `response_code` int DEFAULT NULL,
  `response_result` longtext,
  `status_code` int DEFAULT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_operationlog_creator_id_75ee7a2c_fk_system_userinfo_id` (`creator_id`),
  KEY `system_operationlog_dept_belong_id_54a2fdb4_fk_system_de` (`dept_belong_id`),
  KEY `system_operationlog_modifier_id_898ff5c3_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_operationlog_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_operationlog_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_operationlog_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_systemconfig
-- ----------------------------
DROP TABLE IF EXISTS `system_systemconfig`;
CREATE TABLE `system_systemconfig` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `value` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `access` tinyint(1) NOT NULL,
  `key` varchar(255) NOT NULL,
  `inherit` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `system_systemconfig_creator_id_ec1b6623_fk_system_userinfo_id` (`creator_id`),
  KEY `system_systemconfig_dept_belong_id_cc62784e_fk_system_de` (`dept_belong_id`),
  KEY `system_systemconfig_modifier_id_1bd40069_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_systemconfig_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_systemconfig_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_systemconfig_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_uploadfile
-- ----------------------------
DROP TABLE IF EXISTS `system_uploadfile`;
CREATE TABLE `system_uploadfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `filepath` varchar(100) DEFAULT NULL,
  `file_url` varchar(255) DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  `filesize` int NOT NULL,
  `mime_type` varchar(255) NOT NULL,
  `md5sum` varchar(36) NOT NULL,
  `is_tmp` tinyint(1) NOT NULL,
  `is_upload` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_uploadfile_creator_id_77515c31_fk_system_userinfo_id` (`creator_id`),
  KEY `system_uploadfile_dept_belong_id_6fc03bb4_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_uploadfile_modifier_id_9c19d4a8_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_uploadfile_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_uploadfile_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_uploadfile_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo`;
CREATE TABLE `system_userinfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `mode_type` smallint NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `nickname` varchar(150) NOT NULL,
  `gender` int NOT NULL,
  `phone` varchar(16) NOT NULL,
  `email` varchar(254) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `dept_id` char(32) DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `system_userinfo_dept_id_58621eca_fk_system_deptinfo_id` (`dept_id`),
  KEY `system_userinfo_dept_belong_id_3055ec74_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_userinfo_creator_id_300bf994_fk_system_userinfo_id` (`creator_id`),
  KEY `system_userinfo_modifier_id_439b401f_fk_system_userinfo_id` (`modifier_id`),
  KEY `system_userinfo_phone_87b78cba` (`phone`),
  KEY `system_userinfo_email_bf1d19b4` (`email`),
  CONSTRAINT `system_userinfo_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userinfo_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_userinfo_ibfk_3` FOREIGN KEY (`dept_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_userinfo_ibfk_4` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo_groups
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo_groups`;
CREATE TABLE `system_userinfo_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userinfo_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userinfo_groups_userinfo_id_group_id_2daed2e0_uniq` (`userinfo_id`,`group_id`),
  KEY `system_userinfo_groups_group_id_fb65f4c7_fk_auth_group_id` (`group_id`),
  CONSTRAINT `system_userinfo_groups_ibfk_1` FOREIGN KEY (`userinfo_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo_roles
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo_roles`;
CREATE TABLE `system_userinfo_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userinfo_id` bigint NOT NULL,
  `userrole_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userinfo_roles_userinfo_id_userrole_id_f613220a_uniq` (`userinfo_id`,`userrole_id`),
  KEY `system_userinfo_roles_userrole_id_19a0aa90_fk_system_userrole_id` (`userrole_id`),
  CONSTRAINT `system_userinfo_roles_ibfk_1` FOREIGN KEY (`userinfo_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userinfo_roles_ibfk_2` FOREIGN KEY (`userrole_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo_rules
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo_rules`;
CREATE TABLE `system_userinfo_rules` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userinfo_id` bigint NOT NULL,
  `datapermission_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userinfo_rules_userinfo_id_datapermissi_c68fd319_uniq` (`userinfo_id`,`datapermission_id`),
  KEY `system_userinfo_rule_datapermission_id_3795a994_fk_system_da` (`datapermission_id`),
  CONSTRAINT `system_userinfo_rules_ibfk_1` FOREIGN KEY (`datapermission_id`) REFERENCES `system_datapermission` (`id`),
  CONSTRAINT `system_userinfo_rules_ibfk_2` FOREIGN KEY (`userinfo_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userinfo_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `system_userinfo_user_permissions`;
CREATE TABLE `system_userinfo_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userinfo_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userinfo_user_per_userinfo_id_permission_i_159f729d_uniq` (`userinfo_id`,`permission_id`),
  KEY `system_userinfo_user_permission_id_d9df19b5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `system_userinfo_user_permissions_ibfk_2` FOREIGN KEY (`userinfo_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userloginlog
-- ----------------------------
DROP TABLE IF EXISTS `system_userloginlog`;
CREATE TABLE `system_userloginlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `browser` varchar(64) DEFAULT NULL,
  `system` varchar(64) DEFAULT NULL,
  `agent` varchar(128) DEFAULT NULL,
  `login_type` smallint NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_userloginlog_creator_id_fb430637_fk_system_userinfo_id` (`creator_id`),
  KEY `system_userloginlog_dept_belong_id_113d206c_fk_system_de` (`dept_belong_id`),
  KEY `system_userloginlog_modifier_id_d7c59c97_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_userloginlog_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userloginlog_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_userloginlog_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userpersonalconfig
-- ----------------------------
DROP TABLE IF EXISTS `system_userpersonalconfig`;
CREATE TABLE `system_userpersonalconfig` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `value` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `access` tinyint(1) NOT NULL,
  `key` varchar(255) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  `owner_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userpersonalconfig_owner_id_key_f59b810c_uniq` (`owner_id`,`key`),
  KEY `system_userpersonalc_creator_id_0a83a399_fk_system_us` (`creator_id`),
  KEY `system_userpersonalc_dept_belong_id_43885b3f_fk_system_de` (`dept_belong_id`),
  KEY `system_userpersonalc_modifier_id_6553e630_fk_system_us` (`modifier_id`),
  CONSTRAINT `system_userpersonalconfig_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userpersonalconfig_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_userpersonalconfig_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userpersonalconfig_ibfk_4` FOREIGN KEY (`owner_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userrole
-- ----------------------------
DROP TABLE IF EXISTS `system_userrole`;
CREATE TABLE `system_userrole` (
  `id` char(32) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `name` varchar(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator_id` bigint DEFAULT NULL,
  `dept_belong_id` char(32) DEFAULT NULL,
  `modifier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `system_userrole_creator_id_27e40be6_fk_system_userinfo_id` (`creator_id`),
  KEY `system_userrole_dept_belong_id_9b97618d_fk_system_deptinfo_id` (`dept_belong_id`),
  KEY `system_userrole_modifier_id_c682499b_fk_system_userinfo_id` (`modifier_id`),
  CONSTRAINT `system_userrole_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_userinfo` (`id`),
  CONSTRAINT `system_userrole_ibfk_2` FOREIGN KEY (`dept_belong_id`) REFERENCES `system_deptinfo` (`id`),
  CONSTRAINT `system_userrole_ibfk_3` FOREIGN KEY (`modifier_id`) REFERENCES `system_userinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for system_userrole_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_userrole_menu`;
CREATE TABLE `system_userrole_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userrole_id` char(32) NOT NULL,
  `menu_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_userrole_menu_userrole_id_menu_id_533db074_uniq` (`userrole_id`,`menu_id`),
  KEY `system_userrole_menu_menu_id_b6b2d65f_fk_system_menu_id` (`menu_id`),
  CONSTRAINT `system_userrole_menu_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`),
  CONSTRAINT `system_userrole_menu_ibfk_2` FOREIGN KEY (`userrole_id`) REFERENCES `system_userrole` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
