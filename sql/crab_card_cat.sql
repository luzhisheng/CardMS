DROP TABLE IF EXISTS `crab_card_cat`;

CREATE TABLE `crab_card_cat` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL DEFAULT '' COMMENT '类别名称',
    `weight` tinyint(4) NOT NULL DEFAULT '1' COMMENT '权重',
    `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态1：有效0：无效',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='蟹卡分类';
