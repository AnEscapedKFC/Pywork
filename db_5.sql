/*
 Navicat Premium Data Transfer

 Source Server         : db_1
 Source Server Type    : MySQL
 Source Server Version : 80100 (8.1.0)
 Source Host           : localhost:3306
 Source Schema         : db_5

 Target Server Type    : MySQL
 Target Server Version : 80100 (8.1.0)
 File Encoding         : 65001

 Date: 27/05/2024 22:10:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for email_captcha
-- ----------------------------
DROP TABLE IF EXISTS `email_captcha`;
CREATE TABLE `email_captcha`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `captcha` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '验证码',
  `time` datetime NULL DEFAULT NULL,
  `used` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of email_captcha
-- ----------------------------
INSERT INTO `email_captcha` VALUES (10, '2061398880@qq.com', '0959', '2024-04-23 16:46:59', 0);

-- ----------------------------
-- Table structure for goods_information
-- ----------------------------
DROP TABLE IF EXISTS `goods_information`;
CREATE TABLE `goods_information`  (
  `owner` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `size` double NOT NULL,
  `time` datetime NULL DEFAULT NULL,
  `good_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `Key_Word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `isForsale` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `pkey_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MerkleTree_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci NOT NULL,
  `key_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`, `good_hash`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of goods_information
-- ----------------------------
INSERT INTO `goods_information` VALUES ('1', '1', 1, '2024-05-21 14:56:20', '1', 1.00, '1', '0', 0, '14', '1', '1');

-- ----------------------------
-- Table structure for judge
-- ----------------------------
DROP TABLE IF EXISTS `judge`;
CREATE TABLE `judge`  (
  `time` datetime NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of judge
-- ----------------------------

-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NULL DEFAULT '0',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bg_0900_ai_ci NOT NULL,
  `money` decimal(10, 2) NULL DEFAULT 100.00,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin NULL DEFAULT NULL,
  `pwd1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin NULL DEFAULT NULL COMMENT '一级密码，与前半段哈希值匹配',
  `pwd2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin NULL DEFAULT NULL COMMENT '二级密码，作为AES密钥',
  PRIMARY KEY (`address`) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of person
-- ----------------------------
INSERT INTO `person` VALUES ('KFC', '0xE524aE3543AEf64ff3FBFCAf2419408888Ca6153', 0.00, '2061398880@qq.com', '8d969eef6ecad3c2', '9a3a629280e686cf');
INSERT INTO `person` VALUES ('1dwdw00', 'wffwfw0111', 0.00, '1111', '1', '2');

-- ----------------------------
-- Table structure for person_address
-- ----------------------------
DROP TABLE IF EXISTS `person_address`;
CREATE TABLE `person_address`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `public_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `private_key` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'AES加密后的sc\r\n',
  PRIMARY KEY (`public_key`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of person_address
-- ----------------------------
INSERT INTO `person_address` VALUES ('KFC', '0xE524aE3543AEf64ff3FBFCAf2419408888Ca6153', 'b\"\\xd2\\x9co\\xc6Ch\\xea\\x1c\\xc1\\xe0\\xec\\x15V\\xc9\\x9c\\xa0\\xf6\\x04\\xf9\\x8b\\x00\\x92\\x86+\\n\\xd0\\xdaA\\xbd(\\xc1)2\\x8b\\xaf\\xc0\\xa7\\x9f\\x89\\x16\\xf3lK.\\xc3\\xbf\\xe4&;_zH\\xf5!\\x80\\xee\\x13|\\xfb\\x82Ub\\xac\\x9d4P^\\xca\\xf2y\\xb4q\\xd2\\x02\\xc8Xj\\xa1EJ\\x9e\\xe3\\xb8\\x81\\xa0\\x150!W\\xc2\'\\xf7\\xb7\\xb0\\xa5K\"');
INSERT INTO `person_address` VALUES ('1dwdw00', 'wffwfw0111', 'ssss1');

-- ----------------------------
-- Table structure for transcation
-- ----------------------------
DROP TABLE IF EXISTS `transcation`;
CREATE TABLE `transcation`  (
  `seller` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `buyer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `good_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `time` datetime NULL DEFAULT NULL,
  `price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tradehash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`tradehash`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of transcation
-- ----------------------------
INSERT INTO `transcation` VALUES ('1', '0xE524aE3543AEf64ff3FBFCAf2419408888Ca6153', '111', '2024-03-28 23:39:35', '1.00', '0x609328f9d12a6676e58b7de044fb6364f0678f76e0b76202bb9dae645bae91ca');
INSERT INTO `transcation` VALUES ('1', '0xE524aE3543AEf64ff3FBFCAf2419408888Ca6153', '1.txt', '2024-04-07 22:57:30', '1.00', '0xb47e9b1802a0b9d60c553d925cccb151b6cc8b98e794b962865ca09137a6e73f');

SET FOREIGN_KEY_CHECKS = 1;
