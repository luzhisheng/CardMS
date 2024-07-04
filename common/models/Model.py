from werkzeug.security import generate_password_hash, check_password_hash
from application import db
from flask_login import UserMixin
import datetime


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

    status_mapping = {
        "1": "正常",
        "-1": "已删除"
    }

    @property
    def status_desc(self):
        return self.status_mapping[str(self.status)]


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


class CardStockChangeLog(db.Model):
    """
    数据库模型类，表示食品库存变动日志表。

    属性:
        id (int): 主键，自增。
        food_id (int): 食品ID，用于标识是哪种食品，不能为空。
        unit (int): 变动单位，不能为空，默认为 0。
        total_stock (int): 变动后的总库存，不能为空，默认为 0。
        note (str): 备注信息，不能为空，默认为空字符串。
        created_time (datetime): 记录创建时间，不能为空，默认为当前时间。
    """
    __tablename__ = 'card_stock_change_log'

    id = db.Column(db.Integer, primary_key=True, comment='主键')
    card_id = db.Column(db.Integer, nullable=False, index=True, comment='卡券ID')
    unit = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), comment='变动单位')
    total_stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), comment='总库存')
    note = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), comment='备注')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), comment='创建时间')

    @staticmethod
    def add_log(card_id, unit, total_stock, note):
        """添加库存变动日志"""
        log = CardStockChangeLog(
            card_id=card_id,
            unit=unit,
            total_stock=total_stock,
            note=note,
            created_time=datetime.datetime.now()
        )
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def get_logs(card_id, limit=10):
        """获取最新的库存变动日志"""
        return CardStockChangeLog.query.filter_by(card_id=card_id).order_by(
            CardStockChangeLog.created_time.desc()).limit(limit).all()


class User(UserMixin, db.Model):
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
    login_pwd = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='登录密码')
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(),
                           info='登录密码的随机加密秘钥')
    role_management_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='角色表的id')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1：有效 0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    def get_id(self):
        return str(self.uid)

    def set_password(self, password):
        # 设置密码
        self.login_pwd = generate_password_hash(password)

    def check_password(self, password):
        # 验证密码
        return check_password_hash(self.login_pwd, password)

    status_mapping = {
        "1": "正常",
        "-1": "已删除"
    }

    @property
    def status_desc(self):
        return self.status_mapping[str(self.status)]

    @property
    def sex_desc(self):
        sex_map = {
            "1": "男",
            "2": "女",
            "0": "没填写",
        }
        return sex_map[str(self.sex)]


class RoleManagement(db.Model):
    """
    角色管理表
    """
    __tablename__ = 'role_management'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    role_name = db.Column(db.String(100), nullable=False, comment='角色名称')
    creator = db.Column(db.String(100), nullable=False, comment='创建人')
    status = db.Column(db.Integer, nullable=False, default=1, comment='1：有效 0：无效')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(),
                             comment='创建时间')

    permissions = db.relationship('Permission', secondary='role_permissions',
                                  backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'<RoleManagement {self.role_name}>'


class Permission(db.Model):
    """
    权限表
    """
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='权限ID')
    name = db.Column(db.String(100), nullable=False, comment='权限名称')
    description = db.Column(db.String(255), comment='权限描述')

    def __repr__(self):
        return f'<Permission {self.name}>'


class RolePermission(db.Model):
    """
    角色权限关联表
    """
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('role_management.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)


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

    status_mapping = {
        "1": "正常",
        "-1": "已删除"
    }

    @property
    def status_desc(self):
        return self.status_mapping[str(self.status)]

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

    @property
    def address_all(self):
        address_all = self.province_str + self.city_str + self.area_str + self.address
        return address_all


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
        db.Index('idx_member_id', 'member_id'),
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
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='订单状态')  # 新增的状态字段
    express_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='快递状态')
    express_address_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='快递地址ID')
    express_info = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='快递信息')
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='评论状态')
    pay_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='支付时间')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')

    items = db.relationship('PayOrderItem', back_populates='order')

    @property
    def order_number(self):
        order_number = self.created_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number

    status_mapping = {
        0: "订单关闭",
        1: "支付成功",
        -8: "待支付",
        -7: "待发货",
        -6: "已发货",
        -5: "待确认",
        -4: "待评价",
        -3: "申请售后",
        -2: "已退款"
    }

    @property
    def status_desc(self):
        return self.status_mapping.get(self.status, "未知状态")

    def update_status(self):
        item_statuses = [item.status for item in self.items]

        if all(status == PayOrderItem.STATUS_CLOSED for status in item_statuses):
            self.status = 0
        elif any(status == PayOrderItem.STATUS_REFUNDING for status in item_statuses):
            self.status = -3
        elif all(status == PayOrderItem.STATUS_PAID for status in item_statuses):
            self.status = 1
        elif any(status == PayOrderItem.STATUS_PENDING for status in item_statuses):
            self.status = -8
        elif all(status == PayOrderItem.STATUS_REFUNDED for status in item_statuses):
            self.status = -2
        elif all(status == PayOrderItem.STATUS_TO_SHIP for status in item_statuses):
            self.status = -7
        elif all(status == PayOrderItem.STATUS_SHIPPED for status in item_statuses):
            self.status = -6
        elif all(status == PayOrderItem.STATUS_TO_CONFIRM for status in item_statuses):
            self.status = -5
        elif all(status == PayOrderItem.STATUS_TO_COMMENT for status in item_statuses):
            self.status = -4
        else:
            self.status = 0


class PayOrderItem(db.Model):
    """
    订单交易具体条目信息表
    """
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True, info='订单项ID')
    pay_order_id = db.Column(db.Integer, db.ForeignKey('pay_order.id'), nullable=False, index=True,
                             server_default=db.FetchedValue(), info='支付订单ID')
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='会员ID')
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='数量')
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='价格')
    card_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='卡片ID')
    note = db.Column(db.Text, nullable=False, info='备注')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='状态')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')

    order = db.relationship('PayOrder', back_populates='items')

    status_mapping = {
        0: "订单关闭",
        1: "支付成功",
        -8: "待支付",
        -7: "待发货",
        -6: "已发货",
        -5: "待确认",
        -4: "待评价",
        -3: "申请售后",
        -2: "已退款"
    }

    @property
    def status_desc(self):
        return self.status_mapping.get(self.status, "未知状态")


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


class SysLog(db.Model):
    """
    系统日志表
    """
    __tablename__ = 'sys_logs'
    __table_args__ = (
        db.Index('idx_nickname_account_id', 'nickname', 'account_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='统计ID')
    nickname = db.Column(db.String(50), nullable=True, comment='登录用户名')
    account_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='账户ID/会员ID')
    account_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(),
                             info='账号类型：1-管理，2-会员')
    operation = db.Column(db.String(50), nullable=True, comment='用户操作')
    method = db.Column(db.String(200), nullable=True, comment='请求方法')
    params = db.Column(db.String(5000), nullable=True, comment='请求参数')
    time = db.Column(db.BigInteger, nullable=False, comment='执行时长(毫秒)')
    ip = db.Column(db.String(64), nullable=True, comment='IP地址')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp(),
                             comment='日志记录时间')

    account_type_mapping = {
        1: "管理",
        2: "会员"
    }

    @property
    def account_type_desc(self):
        return self.account_type_mapping.get(self.account_type, "未知类型")

    operation_mapping = {
        "/finance/pay-info": "订单信息",
        "/finance/account": "财务流水",
        "/finance/index": "订单列表",
        "/member/info": "会员信息",
        "/member/set": "会员设置",
        "/member/comment": "会员评论",
        "/member/index": "会员列表",
        "/card/cat": "卡券分类",
        "/card/index": "卡券列表",
        "/card/info": "卡券信息",
        "/card/set": "卡券设置",
        "/card/cat-set": "卡券分类设置",
        "/account/index": "账户列表",
        "/account/info": "账户信息",
        "/account/set": "账号设置",
        "/sys/index": "用户行为列表",
        "/stat/index": "财务统计",
        "/stat/cards": "售卖统计",
        "/stat/member": "会员消费统计",
        "/stat/share": "分享统计",
        "/account/role": "角色管理"
    }

    @property
    def operation_desc(self):
        return self.operation_mapping.get(self.operation, "未知类型")
