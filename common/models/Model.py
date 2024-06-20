from application import db
from application import app


class Card(db.Model):
    """
    卡券信息表
    """
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='分类id')
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='卡券名称')
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='售卖金额')
    main_image = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='主图')
    summary = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue(), info='描述')
    stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='库存量')
    tags = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='tag关键字以","连接')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态1有效0无效')
    month_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='月销售数量')
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='总销售量')
    view_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='总浏览次数')
    comment_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='总评论量')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后插入时间')


class CardCat(db.Model):
    """
    卡券分类表
    """
    __tablename__ = 'card_cat'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, server_default=db.FetchedValue(), info='类别名称')
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='权重')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态1：有效0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')


class User(db.Model):
    """
    管理员账户表
    """
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True, info='用户uid')
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='用户名')
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='手机号码')
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='邮箱地址')
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1：男 2：女 0：没填写')
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue(), info='头像')
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue(),
                           info='登录用户名')
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='登录密码')
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(),
                           info='登录密码的随机加密秘钥')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1：有效 0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    @property
    def sex_desc(self):
        sex_map = {
            "1": "男",
            "2": "女",
            "0": "没填写",
        }
        return sex_map[str(self.sex)]


class Member(db.Model):
    """
    会员信息表
    """
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True, info='会员ID')
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='昵称')
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue(), info='手机号')
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='性别：0-未知，1-男，2-女')
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='头像URL')
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='加密盐值')
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='注册IP地址')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态：1-正常，-1-已删除')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')

    # Establishing relationship
    comments = db.relationship('MemberComments', backref='member', lazy=True)

    @property
    def status_desc(self):
        status_mapping = {
            "1": "正常",
            "-1": "已删除"
        }
        return status_mapping[str(self.status)]

    @property
    def sex_desc(self):
        sex_mapping = {
            "0": "未知",
            "1": "男",
            "2": "女"
        }
        return sex_mapping[str(self.sex)]


class MemberAddress(db.Model):
    """
    会员地址表
    """
    __tablename__ = 'member_address'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True, info='地址ID')
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='会员ID')
    nickname = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='昵称')
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue(), info='手机号')
    province_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='省份ID')
    province_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue(), info='省份名称')
    city_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='城市ID')
    city_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue(), info='城市名称')
    area_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='区域ID')
    area_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue(), info='区域名称')
    address = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='详细地址')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态')
    is_default = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否默认地址')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')


class MemberComments(db.Model):
    """
    会员评论表
    """
    __tablename__ = 'member_comments'

    id = db.Column(db.Integer, primary_key=True, info='评论ID')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False, index=True,
                          server_default=db.FetchedValue(), info='会员ID')
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False, server_default=db.FetchedValue(),
                        info='卡片ID')
    pay_order_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='支付订单ID')
    score = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='评分（0到10）')
    content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='评论内容')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='评论创建时间')

    @property
    def score_desc(self):
        score_map = {
            "10": "好评",
            "6": "中评",
            "0": "差评",
        }
        return score_map[str(self.score)]


class PayOrder(db.Model):
    """
    订单的详细信息表
    """
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True, info='订单ID')
    order_sn = db.Column(db.String(40), nullable=False, unique=True, server_default=db.FetchedValue(), info='订单编号')
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='会员ID')
    total_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='总价格')
    yun_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='运费')
    pay_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='支付价格')
    pay_sn = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue(), info='支付编号')
    prepay_id = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue(), info='预支付ID')
    note = db.Column(db.Text, nullable=False, info='备注')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='订单状态')
    express_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='快递状态')
    express_address_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='快递地址ID')
    express_info = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='快递信息')
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='评论状态')
    pay_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='支付时间')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')

    @property
    def pay_status(self):
        tmp_status = self.status
        if self.status == 1:
            tmp_status = self.express_status
            if self.express_status == 1 and self.comment_status == 0:
                tmp_status = -5
            if self.express_status == 1 and self.comment_status == 1:
                tmp_status = 1
        return tmp_status

    @property
    def status_desc(self):
        pay_status_display_mapping = {
            "0": "订单关闭",
            "1": "支付成功",
            "-8": "待支付",
            "-7": "待发货",
            "-6": "待确认",
            "-5": "待评价"
        }
        return pay_status_display_mapping.get(str(self.pay_status), "未知状态")

    @property
    def order_number(self):
        order_number = self.created_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number


class PayOrderItem(db.Model):
    """
    订单交易具体条目信息表
    """
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True, info='订单项ID')
    pay_order_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(),
                             info='支付订单ID')
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='会员ID')
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='数量')
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='价格')
    card_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='卡片ID')
    note = db.Column(db.Text, nullable=False, info='备注')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')


class StatDailySite(db.Model):
    """
    站点每日统计信息表
    """
    __tablename__ = 'stat_daily_site'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    date = db.Column(db.Date, nullable=False, index=True, comment='统计日期')
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(),
                                comment='总支付金额')
    total_member_count = db.Column(db.Integer, nullable=False, comment='总会员数')
    total_new_member_count = db.Column(db.Integer, nullable=False, comment='新增会员数')
    total_order_count = db.Column(db.Integer, nullable=False, comment='总订单数')
    total_shared_count = db.Column(db.Integer, nullable=False, comment='总分享数')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), comment='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), comment='创建时间')


class StatDailyMember(db.Model):
    """
    站点每日会员分享信息表
    """
    __tablename__ = 'stat_daily_member'
    __table_args__ = (
        db.Index('idx_date_member_id', 'date', 'member_id'),
    )

    id = db.Column(db.Integer, primary_key=True, info='每日会员统计ID')
    date = db.Column(db.Date, nullable=False, info='统计日期')
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='会员ID')
    total_shared_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='总分享数')
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='总支付金额')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')


class StatDailyCard(db.Model):
    """
    站点每日卡券统计信息表
    """
    __tablename__ = 'stat_daily_card'
    __table_args__ = (
        db.Index('date_card_id', 'date', 'card_id'),
    )

    id = db.Column(db.Integer, primary_key=True, info='每日卡片统计ID')
    date = db.Column(db.Date, nullable=False, info='统计日期')
    card_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='卡片ID')
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='总数量')
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='总支付金额')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')
