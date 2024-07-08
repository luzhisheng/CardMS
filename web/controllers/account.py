from flask import Blueprint, request, redirect, g, jsonify
from common.libs.Helper import optRender, genPwd, paging, generateRandomNumber, permission_required
from common.models.Model import User, SysLog, Role, RolePermission, Permission
from sqlalchemy import or_, func
from application import db
from sqlalchemy.exc import IntegrityError

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
    role_ids = [user.role_id for user in users]
    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    role_dict = {role.id: role.name for role in roles}

    for user in users:
        role_name = role_dict.get(user.role_id, "未知角色")
        user.role = role_name

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
            rep["user_info"] = user_info
        roles = Role.query.all()
        role_dict = {role.id: role.role_name for role in roles}
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

        role_id = request.values.get('role_id')
        if role_id is None or len(role_id) < 1:
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
        user_info.role_id = role_id
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


@route_account.route("/role_ops", methods=["POST"])
def role_ops():
    req = request.values
    if req.get('act') == "remove":
        resp = {
            'code': 200,
            'msg': "删除角色成功",
            "data": {}
        }
        role = Role.query.filter_by(id=req.get('id')).first()
        role.status = -1
        db.session.add(role)
        db.session.commit()
        return jsonify(resp)
    else:
        resp = {
            'code': 200,
            'msg': "恢复角色成功",
            "data": {}
        }
        role = Role.query.filter_by(id=req.get('id')).first()
        role.status = 1
        db.session.add(role)
        db.session.commit()
        return jsonify(resp)


@route_account.route("/role", methods=["GET", "POST"])
def role():
    query = db.session.query(Role)

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    # 使用外连接查询每个角色的分配人数
    role_with_count_query = (
        query
        .outerjoin(User, Role.id == User.role_id)
        .with_entities(Role, func.count(User.uid).label('user_count'))
        .group_by(Role.id)
    )

    # 获取查询结果
    role_with_count = role_with_count_query.all()

    # 格式化结果，包括权限信息
    role_list = [
        {
            'role': {
                'id': role.id,
                'name': role.name,
                'creator': role.creator,
                'created_time': role.created_time,
                'status': role.status,
                'permissions': ', '.join([perm.description for perm in role.permissions if perm.description])
            },
            'user_count': user_count,
        }
        for role, user_count in role_with_count
    ]

    resp = {
        'list': role_list,
        'search_con': request.values,
        'status_mapping': User.status_mapping,
        "current": "role"
    }
    return optRender('account/role.html', resp)


@route_account.route("/role_set", methods=["GET", "POST"])
def role_set():
    if request.method == "GET":
        rep = {
            "role": {
                "assigned_people_count": 0,
                "selected_permissions": []
            },
            "current": "role"
        }
        if request.values.get('id'):
            role = Role.query.filter_by(id=request.values.get('id')).first()
            if role:
                selected_permissions = [perm.id for perm in role.permissions]
                assigned_people_count = RolePermission.query.filter_by(permission_id=role.id).count()
                rep["role"] = role
                rep["role"].assigned_people_count = assigned_people_count
                rep["role"].selected_permissions = selected_permissions
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

        if request.values.get('id'):
            # 修改数据
            role = Role.query.filter_by(id=int(request.values.get('id'))).first()
            if not role:
                resp['code'] = -1
                resp['msg'] = "角色不存在"
                return jsonify(resp)
            resp['msg'] = "修改角色成功"
        else:
            # 新增数据
            role = Role()
            resp['msg'] = "新增角色成功"

        # 获取权限ID
        permissions_id = request.values.getlist('permissions_id[]')
        # 更新角色的权限
        role.permissions.clear()  # 清空现有权限
        for perm_id in permissions_id:
            permission = Permission.query.get(perm_id)
            if permission:
                role.permissions.append(permission)

        db.session.add(role)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            resp['code'] = -1
            resp['msg'] = f"数据库错误: {str(e)}"
            return jsonify(resp)
        return jsonify(resp)


@route_account.route("/permission", methods=["GET", "POST"])
def permissions():
    query = Permission.query

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    permission = query.all()
    resp = {
        'list': permission,
        'search_con': request.values,
        'status_mapping': Permission.status_mapping,
        "current": "permission"
    }
    return optRender('account/permission.html', resp)


@route_account.route("/permission_ops", methods=["POST"])
def permission_ops():
    req = request.values
    if req.get('act') == "remove":
        resp = {
            'code': 200,
            'msg': "删除角色成功",
            "data": {}
        }
        permission = Permission.query.filter_by(id=req.get('id')).first()
        permission.status = -1
        db.session.add(permission)
        db.session.commit()
        return jsonify(resp)
    else:
        resp = {
            'code': 200,
            'msg': "恢复角色成功",
            "data": {}
        }
        permission = Permission.query.filter_by(id=req.get('id')).first()
        permission.status = 1
        db.session.add(permission)
        db.session.commit()
        return jsonify(resp)


@route_account.route("/permission_set", methods=["GET", "POST"])
def permission_set():
    if request.method == "GET":
        rep = {
            "permission": "",
            "current": "permission"
        }
        if request.values.get('id'):
            permission = Permission.query.filter_by(id=request.values.get('id')).first()
            if permission:
                rep["permission"] = permission
        return optRender('account/permission_set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增权限成功",
            "data": {}
        }
        name = request.values.get('name')
        if name is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的权限名称~~"
            return jsonify(resp)

        description = request.values.get('description')
        if description is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的权限描述~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            permission = Permission.query.filter_by(id=int(request.values.get('id'))).first()
            if not permission:
                resp['code'] = -1
                resp['msg'] = "权限不存在"
                return jsonify(resp)
            resp['msg'] = "修改权限成功"
        else:
            # 新增数据
            permission = Permission()
            resp['msg'] = "新增权限成功"

        permission.name = name
        permission.description = description
        db.session.add(permission)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            resp['code'] = -1
            resp['msg'] = f"数据库错误: {str(e)}"
            return jsonify(resp)
        return jsonify(resp)
