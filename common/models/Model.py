from application import db


class Cards(db.Model):
    __tablename__ = 'crabs'

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
