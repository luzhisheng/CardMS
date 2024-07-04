from flask import Blueprint, request, redirect, g, jsonify
from common.libs.Helper import optRender, genPwd, paging, generateRandomNumber
from common.models.Model import User, SysLog, RoleManagement, RolePermission
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
    users = query.order_by(User.uid.desc()).all()[offset:limit]

    # 拼接角色数据
    role_ids = [user.role_management_id for user in users]
    roles = RoleManagement.query.filter(RoleManagement.id.in_(role_ids)).all()
    role_dict = {role.id: role.role_name for role in roles}

    for user in users:
        role_name = role_dict.get(user.role_management_id, "未知角色")
        user.role_management = role_name

    resp = {
        'user_list': users,
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
            'role_mapping': {},
            "current": "index"
        }
        if request.values.get('id'):
            user_info = User.query.filter_by(uid=request.values.get('id')).first()
            role_management = RoleManagement.query.all()
            role_dict = {role.id: role.role_name for role in role_management}
            rep["user_info"] = user_info
            rep["role_mapping"] = role_dict
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

        role_management_id = request.values.get('role_management_id')
        if role_management_id is None or len(role_management_id) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的角色~~"
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
        user_info.role_management_id = role_management_id
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


@route_account.route("/role_set", methods=["GET", "POST"])
def role_set():
    if request.method == "GET":
        rep = {
            "role_management": {
                "assigned_people_count": 0,
            },
            "current": "role"
        }
        if request.values.get('id'):
            role_management = RoleManagement.query.filter_by(id=request.values.get('id')).first()
            assigned_people_count = RolePermission.query.filter_by(permission_id=role_management.id).count()
            rep["role_management"] = role_management
            rep["role_management"].assigned_people_count = assigned_people_count
        return optRender('account/role_set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增角色成功",
            "data": {}
        }
        role_name = request.values.get('role_name')
        if role_name is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的角色名称~~"
            return jsonify(resp)

        creator = request.values.get('creator')
        if creator is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的创建人~~"
            return jsonify(resp)

        assigned_people_count = request.values.get('assigned_people_count')
        if creator is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的分配人数~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            role_management = RoleManagement.query.filter_by(id=int(request.values.get('id'))).first()
            resp['msg'] = "修改用户成功"
        else:
            # 新增数据
            role_management = RoleManagement()
        role_management.role_name = role_name
        role_management.assigned_people_count = assigned_people_count
        role_management.creator = creator
        db.session.add(role_management)
        db.session.commit()
        return jsonify(resp)
