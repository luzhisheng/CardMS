from flask import Blueprint, request, redirect, g, jsonify
from common.libs.Helper import optRender, genPwd, paging, generateRandomNumber
from common.models.Model import User, SysLog, RoleManagement
from sqlalchemy import or_
from application import db

route_account = Blueprint("account_page", __name__)


@route_account.route("/index")
def index():
    query = User.query

    mix_kw = request.values.get('mix_kw')
    if mix_kw:
        # 搜索查询
        rule = or_(User.nickname.ilike(f"%{mix_kw}%"), User.mobile.ilike(f"%{mix_kw}%"))
        query = query.filter(rule)

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    user_list = query.order_by(User.uid.desc()).all()[offset:limit]
    resp = {
        'user_list': user_list,
        'pages': pages,
        'search_con': request.values,
        'status_mapping': User.status_mapping,
        "current": "index"
    }
    return optRender('account/index.html', resp)


@route_account.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        rep = {
            "user_info": "",
            'sex_mapping': {
                "0": "没填写",
                "1": "男",
                "2": "女"
            },
            "current": "index"
        }
        if request.values.get('id'):
            user_info = User.query.filter_by(uid=request.values.get('id')).first()
            rep["user_info"] = user_info
        return optRender('account/set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增用户成功",
            "data": {}
        }
        avatar = request.values.get('avatar')
        if avatar is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的头像~~"
            return jsonify(resp)

        nickname = request.values.get('nickname')
        if nickname is None or len(nickname) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的姓名~~"
            return jsonify(resp)

        mobile = request.values.get('mobile')
        if mobile is None or len(mobile) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的手机号码~~"
            return jsonify(resp)

        email = request.values.get('email')
        if email is None or len(email) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的邮箱~~"
            return jsonify(resp)

        sex = request.values.get('sex')
        if sex is None or len(sex) != 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的性别~~"
            return jsonify(resp)

        login_name = request.values.get('login_name')
        if login_name is None or len(login_name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的登录用户名~~"
            return jsonify(resp)

        login_pwd = request.values.get('login_pwd')
        if login_pwd is None or len(login_pwd) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的登录密码~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            user_info = User.query.filter_by(uid=int(request.values.get('id'))).first()
            resp['msg'] = "修改用户成功"
        else:
            # 新增数据
            user_info = User()
        login_salt = generateRandomNumber()
        user_info.avatar = avatar
        user_info.nickname = nickname
        user_info.login_pwd = genPwd(login_pwd, login_salt)
        user_info.login_salt = login_salt
        user_info.mobile = mobile
        user_info.email = email
        user_info.sex = sex
        user_info.login_name = login_name
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_account.route("/info", methods=["GET"])
def info():
    uid = request.values.get('id')
    user_count = User.query.count()
    user_info = User.query.filter_by(uid=uid).first()
    sys_log = SysLog.query.filter_by(account_id=uid).order_by(SysLog.id.desc()).limit(10).all()
    resp = {
        'info': user_info,
        'sys_logs': sys_log,
    }
    # 当输入uid超过最大值重定向第一页
    if int(uid) > user_count:
        return redirect('/account/index')
    return optRender('account/info.html', resp)


@route_account.route("/ops", methods=["POST"])
def ops():
    req = request.values
    if req.get('act') == "remove":
        resp = {
            'code': 200,
            'msg': "删除用户成功",
            "data": {}
        }
        user_info = User.query.filter_by(uid=req.get('id')).first()
        user_info.status = -1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)
    else:
        resp = {
            'code': 200,
            'msg': "恢复用户成功",
            "data": {}
        }
        user_info = User.query.filter_by(uid=req.get('id')).first()
        user_info.status = 1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_account.route("/role", methods=["GET", "POST"])
def role():
    query = RoleManagement.query

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    role_management = query.all()

    resp = {
        'list': role_management,
        'search_con': request.values,
        'status_mapping': User.status_mapping,
        "current": "role"
    }
    return optRender('account/role.html', resp)
