from flask import Blueprint, request, jsonify
from common.libs.Helper import optRender, paging, permission_required
from common.models.Model import SysLog, Setting
from application import db
from sqlalchemy import or_

route_sys = Blueprint('sys_page', __name__)


@route_sys.route("/index", methods=["GET"])
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


@route_sys.route("/setting-set", methods=["GET", "POST"])
@permission_required("setting_set")
def sys_setting_set():
    setting = Setting.query.filter_by(id=1).first()
    if request.method == "GET":
        rep = {
            "info": setting,
            "current": "setting_set",
        }
        return optRender('sys/setting_set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "修改配置信成功",
            "data": {}
        }

        mini_program_code_image = request.values.get('mini_program_code_image')
        if mini_program_code_image is None or len(mini_program_code_image) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的小程序码~~"
            return jsonify(resp)

        public_number_image = request.values.get('public_number_image')
        if public_number_image is None or len(public_number_image) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的公众号码~~"
            return jsonify(resp)

        if not setting:
            setting = Setting()
        setting.mini_program_code_image = mini_program_code_image
        setting.public_number_image = public_number_image
        db.session.add(setting)
        db.session.commit()
        return jsonify(resp)
