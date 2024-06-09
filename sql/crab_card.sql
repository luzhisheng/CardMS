DROP TABLE IF EXISTS `crab_card`;

CREATE TABLE `crab_card`
(
    `id`            int(11) unsigned NOT NULL AUTO_INCREMENT,
    `cat_id`        INT(11) NOT NULL DEFAULT '0' COMMENT '分类id',
    `name`          varchar(100)   NOT NULL DEFAULT '' COMMENT '书籍名称',
    `price`         decimal(10, 2) NOT NULL DEFAULT '0.00' COMMENT '售卖金额',
    `main_image`    VARCHAR(100)   NOT NULL DEFAULT '' COMMENT '主图',
    `summary`       VARCHAR(2000)  NOT NULL DEFAULT '' COMMENT '描述',
    `stock`         INT(11) NOT NULL DEFAULT '0' COMMENT '库存量',
    `tags`          varchar(200)   NOT NULL DEFAULT '' COMMENT 'tag关键字以","连接',
    `status`        tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态1有效0无效',
    `month_count`   int(11) NOT NULL DEFAULT '0' COMMENT '月销售数量',
    `total_count`   INT(11) NOT NULL DEFAULT '0' COMMENT '总销售量',
    `view_count`    INT(11) NOT NULL DEFAULT '0' COMMENT '总浏览次数',
    `comment_count` INT(11) NOT NULL DEFAULT '0' COMMENT '总评论量',
    `updated_time`  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
    `created_time`  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='蟹卡表';
