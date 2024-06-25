from flask import Blueprint, request
from web.controllers.helper import opt_render
from common.models.Model import SysLog
from web.controllers.helper import iPagination
from sqlalchemy import or_

route_sys = Blueprint('sys_page', __name__)


@route_sys.route("/index")
def index():
    count = SysLog.query.count()
    p = request.values.get('p')

    page_size = 20
    if not p:
        page = 1
    else:
        page = int(p)

    params = {
        "total": count,  # 总数
        "page_size": page_size,  # 每页的数量
        "page": int(page),  # 第几页
        "display": 10,
        "url": '/card/index?'
    }
    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page_size * page

    query = SysLog.query

    mix_kw = request.values.get('mix_kw')
    if mix_kw:
        # 搜索查询
        rule = or_(SysLog.nickname.ilike(f"%{mix_kw}%"), SysLog.params.ilike(f"%{mix_kw}%"))
        query = query.filter(rule)

    account_type = request.values.get('account_type')
    if account_type:
        query = query.filter_by(account_type=account_type)

    operation = request.values.get('operation')
    if operation:
        query = query.filter_by(operation=operation)

    pay_list = query.order_by(SysLog.id.desc()).all()[offset:limit]

    resp_data = {
        'list': pay_list,
        'pages': pages,
        'search_con': request.values,
        "current": "index",
        'account_type_mapping': SysLog.account_type_mapping,
        'operation_mapping': SysLog.operation_mapping,
    }
    return opt_render("sys/index.html", resp_data)
