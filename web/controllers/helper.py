from flask import g, render_template
import hashlib
import base64
import random
import re


# 密码加密
def gen_pwd(pwd, salt):
    m = hashlib.md5()
    str = f"{base64.encodebytes(pwd.encode('utf-8'))}-{salt}"
    m.update(str.encode("utf-8"))
    return m.hexdigest()


def generate_random_number(length=4):
    """
    生成指定长度的随机数字字符串，默认长度为4.

    :param length: int, 随机数字字符串的长度
    :return: str, 生成的随机数字字符串
    """
    return "salt" + ''.join([str(random.randint(0, 9)) for _ in range(length)])


# cookie加密
def gene_auth_code(user_info):
    m = hashlib.md5()
    str = f"{user_info.login_name}-{user_info.login_salt}-{user_info.login_pwd}-{user_info.uid}"
    base64.encodebytes(str.encode('utf-8'))
    m.update(str.encode("utf-8"))
    return m.hexdigest()


# 统一渲染方法
def opt_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)


# 分页
def iPagination(params):
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


def is_integer(value):
    """
    判断是为int类型
    """
    try:
        int_value = int(value)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_price(price_str):
    # 使用正则表达式检查价格格式是否正确
    pattern = r'^\d+(\.\d{1,2})?$'
    return re.match(pattern, price_str) is not None


def is_valid_integer_stock(stock_str):
    # 检查价格是否为有效的整数
    try:
        stock = int(stock_str)
        return True
    except ValueError:
        return False
