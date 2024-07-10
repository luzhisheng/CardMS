from flask import Blueprint, request
from common.libs.Helper import optRender, paging, permission_required
from common.models.Model import SysLog
from sqlalchemy import or_

route_sys = Blueprint('sys_page', __name__)


@route_sys.route("/index")
@permission_required("sys_index")
def index():
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

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    sys_log_list = query.order_by(SysLog.id.desc()).all()[offset:limit]

    resp_data = {
        'list': sys_log_list,
        'pages': pages,
        'search_con': request.values,
        "current": "index",
        'account_type_mapping': SysLog.account_type_mapping,
        'operation_mapping': SysLog.operation_mapping,
    }
    return optRender("sys/index.html", resp_data)
