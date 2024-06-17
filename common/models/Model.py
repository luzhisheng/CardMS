from application import db
from application import app


class Cards(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='分类id')
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='书籍名称')
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


class CardsCat(db.Model):
    __tablename__ = 'cards_cat'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, server_default=db.FetchedValue(), info='类别名称')
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='权重')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态1：有效0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')


class User(db.Model):
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


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

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
    __tablename__ = 'member_address'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    province_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    province_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    city_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    city_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    area_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    area_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_default = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class MemberComments(db.Model):
    __tablename__ = 'member_comments'

    id = db.Column(db.Integer, primary_key=True, info='评论ID')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False, index=True,
                          server_default=db.FetchedValue(), info='会员ID')
    cards_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False, server_default=db.FetchedValue(),
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
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True, server_default=db.FetchedValue())
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    total_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    yun_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    pay_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    pay_sn = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    prepay_id = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_address_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_info = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pay_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

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
        return pay_status_display_mapping[str(self.pay_status)]

    @property
    def order_number(self):
        order_number = self.created_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number


class PayOrderItem(db.Model):
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True)
    pay_order_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    cards_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    note = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class StatDailySite(db.Model):
    __tablename__ = 'stat_daily_site'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    total_member_count = db.Column(db.Integer, nullable=False)
    total_new_member_count = db.Column(db.Integer, nullable=False)
    total_order_count = db.Column(db.Integer, nullable=False)
    total_shared_count = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class StatDailyMember(db.Model):
    __tablename__ = 'stat_daily_member'
    __table_args__ = (
        db.Index('idx_date_member_id', 'date', 'member_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_shared_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class StatDailyCards(db.Model):
    __tablename__ = 'stat_daily_cards'
    __table_args__ = (
        db.Index('date_cards_id', 'date', 'cards_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    cards_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
