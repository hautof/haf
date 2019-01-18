/*
Navicat MySQL Data Transfer

Source Server         : 172.7.58.22
Source Server Version : 50724
Source Host           : 172.7.58.22:3306
Source Database       : haf_publish

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2019-01-18 12:11:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for case
-- ----------------------------
DROP TABLE IF EXISTS `case`;
CREATE TABLE `case` (
  `id` int(11) NOT NULL,
  `ids_id` varchar(255) DEFAULT NULL,
  `run` int(255) DEFAULT NULL,
  `dependent` varchar(255) DEFAULT NULL,
  `bench_name` varchar(255) DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `response_id` int(11) DEFAULT NULL,
  `expect_id` int(11) DEFAULT NULL,
  `sqlinfo_id` int(11) DEFAULT NULL,
  `type` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_expect
-- ----------------------------
DROP TABLE IF EXISTS `case_expect`;
CREATE TABLE `case_expect` (
  `id` int(11) NOT NULL,
  `response_id` int(11) DEFAULT NULL,
  `sql_check_func` varchar(255) DEFAULT NULL,
  `sql_response_result` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_ids
-- ----------------------------
DROP TABLE IF EXISTS `case_ids`;
CREATE TABLE `case_ids` (
  `id` int(11) NOT NULL,
  `case_id` int(11) DEFAULT NULL,
  `case_sub_id` int(11) DEFAULT NULL,
  `case_name` varchar(255) DEFAULT NULL,
  `case_api_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_request
-- ----------------------------
DROP TABLE IF EXISTS `case_request`;
CREATE TABLE `case_request` (
  `id` int(11) NOT NULL,
  `header` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `method` varchar(255) DEFAULT NULL,
  `protocol` varchar(255) DEFAULT NULL,
  `host_port` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_response
-- ----------------------------
DROP TABLE IF EXISTS `case_response`;
CREATE TABLE `case_response` (
  `id` int(11) NOT NULL,
  `header` varchar(255) DEFAULT NULL,
  `body` varchar(255) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_sqlinfo
-- ----------------------------
DROP TABLE IF EXISTS `case_sqlinfo`;
CREATE TABLE `case_sqlinfo` (
  `id` int(11) NOT NULL,
  `scripts_id` int(11) DEFAULT NULL,
  `config` varchar(255) DEFAULT NULL,
  `config_id` int(11) DEFAULT NULL,
  `check_list_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_sqlinfo_checklist
-- ----------------------------
DROP TABLE IF EXISTS `case_sqlinfo_checklist`;
CREATE TABLE `case_sqlinfo_checklist` (
  `id` int(11) NOT NULL,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for case_sqlinfo_script
-- ----------------------------
DROP TABLE IF EXISTS `case_sqlinfo_script`;
CREATE TABLE `case_sqlinfo_script` (
  `id` int(11) NOT NULL,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for detail
-- ----------------------------
DROP TABLE IF EXISTS `detail`;
CREATE TABLE `detail` (
  `id` int(11) NOT NULL,
  `suite_id` int(11) DEFAULT NULL,
  `case_name` varchar(255) DEFAULT NULL,
  `result_check_response` varchar(255) DEFAULT NULL,
  `result_check_sql_response` varchar(255) DEFAULT NULL,
  `run_error` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `case_id` int(11) DEFAULT NULL,
  `log_dir` varchar(255) DEFAULT NULL,
  `runner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for main
-- ----------------------------
DROP TABLE IF EXISTS `main`;
CREATE TABLE `main` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration_time` time DEFAULT NULL,
  `passed` int(255) DEFAULT NULL,
  `failed` int(255) DEFAULT NULL,
  `skip` int(255) DEFAULT NULL,
  `error` int(255) DEFAULT NULL,
  `suite_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for suite
-- ----------------------------
DROP TABLE IF EXISTS `suite`;
CREATE TABLE `suite` (
  `id` int(11) NOT NULL,
  `suite_id` int(11) NOT NULL,
  `suite_name` varchar(255) NOT NULL,
  `detail_id` int(11) NOT NULL,
  `summary_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for summary
-- ----------------------------
DROP TABLE IF EXISTS `summary`;
CREATE TABLE `summary` (
  `id` int(11) NOT NULL,
  `suite_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `passed` int(255) DEFAULT NULL,
  `failed` int(255) DEFAULT NULL,
  `skip` int(255) DEFAULT NULL,
  `error` int(255) DEFAULT NULL,
  `all` int(255) DEFAULT NULL,
  `base_url` varchar(255) DEFAULT NULL,
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
