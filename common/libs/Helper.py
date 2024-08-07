from flask import render_template, request, g
from application import app
from common.models.Model import Role, Setting
from flask_login import current_user
from functools import wraps
import datetime
import random
import re


def genPwd(pwd, salt):
    """
    密码拼接
    :param pwd:
    :param salt:
    :return:
    """
    str = f"{pwd}-{salt}"
    return str


def generateRandomNumber(length=4):
    """
    生成指定长度的随机数字字符串，默认长度为4.
    :param length: int, 随机数字字符串的长度
    :return: str, 生成的随机数字字符串
    """
    return "salt" + ''.join([str(random.randint(0, 9)) for _ in range(length)])


def optRender(template, context=None):
    """
    统一渲染方法
    :param template:
    :param context:
    :return:
    """
    if context is None:
        context = {}
    if current_user.is_authenticated:
        context['current_user'] = current_user
    return render_template(template, **context)


def paging(page_size, total, p):
    """
    获取分页的offset，limit，pages
    :param total:
    :param page_size:
    :param p:
    :return:
    """
    if not p:
        page = 1
    else:
        page = int(p)

    params = {
        "total": total,  # 总数
        "page_size": page_size,  # 每页的数量
        "page": int(page),  # 第几页
        "display": 10,
        "url": request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page_size * page
    return pages, offset, limit


def iPagination(params):
    """
    自定义分页类
    :param params:
    :return:
    """
    import math

    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url'].replace("&p=", "")
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page = int(params['page'])
    display = int(params['display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int(math.ceil(display / 2))

    if page - semi > 0:
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages:
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range(ret['from'], ret['end'] + 1)
    return ret


def isInteger(value):
    """
    判断是为int类型
    """
    try:
        int_value = int(value)
        return True
    except (ValueError, TypeError):
        return False


def isValidPrice(price_str):
    """
    使用正则表达式检查价格格式是否正确
    :param price_str:
    :return:
    """
    pattern = r'^\d+(\.\d{1,2})?$'
    return re.match(pattern, price_str) is not None


def isValidIntegerStock(stock_str):
    """
    检查价格是否为有效的整数
    :param stock_str:
    :return:
    """
    try:
        stock = int(stock_str)
        return True
    except ValueError:
        return False


def getCurrentDate():
    """
    获取当前时间
    :param
    :return:
    """
    return datetime.datetime.now()


def getFormatDate(date=None, date_format="%Y-%m-%d %H:%M:%S"):
    """
    获取格式化的时间
    :param date:
    :param date_format:
    :return:
    """
    if date is None:
        date = datetime.datetime.now()

    return date.strftime(date_format)


def getDictFilterField(db_model, select_filed, key_field, id_list):
    """
    根据某个字段获取一个dic出来
    :param db_model:
    :param select_filed:
    :param key_field:
    :param id_list:
    :return:
    """
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    res_list = query.all()
    if not res_list:
        return ret
    for item in res_list:
        if not hasattr(item, key_field):
            break
        if getattr(item, key_field) not in ret:
            ret[getattr(item, key_field)] = []
        ret[getattr(item, key_field)] = item
    return ret


def selectFilterObj(obj, field):
    ret = []
    for item in obj:
        if not hasattr(item, field):
            break
        if getattr(item, field) in ret:
            continue
        ret.append(getattr(item, field))
    return ret


@app.before_request
def load_user_permissions():
    if current_user.is_authenticated:
        role = Role.query.get(current_user.role_id)
        if role:
            g.permissions = [p.name for p in role.permissions]
        else:
            g.permissions = []
    else:
        g.permissions = []


def has_permission(permission):
    """
    判断是否存在权限
    :param permission:
    :return:
    """
    if permission in g.permissions:
        return True
    else:
        return False


@app.context_processor
def utility_processor():
    return dict(has_permission=has_permission)


# 处理 404 错误
@app.errorhandler(404)
def page_not_found(e):
    return optRender("error/403.html")


def permission_required(permission):
    """
    自定义用户权限检查器
    :param permission:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                setting = Setting.query.filter_by(id=1).first()
                rep = {
                    "info": setting,
                    "current": "setting_set",
                }
                return optRender("user/login.html", rep)
            if not has_permission(permission):
                return optRender("error/403.html")
            return f(*args, **kwargs)

        return decorated_function

    return decorator
