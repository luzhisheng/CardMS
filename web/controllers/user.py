from flask import Blueprint, request, jsonify
from flask import make_response, redirect
from flask_login import login_user, current_user, logout_user
from common.libs.Helper import optRender, genPwd, permission_required
from application import db
import json
from common.models.Model import User, Setting

route_user = Blueprint("user_page", __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        setting = Setting.query.filter_by(id=1).first()
        rep = {
            "info": setting
        }
        return optRender("user/login.html", rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "登陆成功",
            "data": {}
        }
        req = request.values
        login_name = req['login_name'] if 'login_name' in req else ''
        login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

        if login_name is None or len(login_name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入正确的用户名/密码-1"
            return jsonify(resp)

        if login_name is None or len(login_pwd) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入正确的用户名/密码-2"
            return jsonify(resp)

        user_info = User.query.filter_by(login_name=login_name).first()
        if not user_info:
            resp['code'] = -1
            resp['msg'] = "请输入正确的用户名/密码-3"
            return jsonify(resp)

        # 比对密码
        if not user_info.check_password(genPwd(login_pwd, user_info.login_salt)):
            resp['code'] = -1
            resp['msg'] = "请输入正确的用户名/密码-4"
            return jsonify(resp)

        if user_info.status != 1:
            resp['code'] = -1
            resp['msg'] = "账号被禁用，请找管理员核实"
            return jsonify(resp)

        # 设置cookie
        response = make_response(json.dumps(resp))
        login_user(user_info)
        return response


@route_user.route("/edit", methods=["GET", "POST"])
@permission_required('edit')
def edit():
    if request.method == "GET":
        return optRender("user/edit.html", {'current': 'edit'})
    else:
        resp = {
            'code': 200,
            'msg': "修改成功",
            "data": {}
        }
        req = request.values
        nickname = req['nickname'] if 'nickname' in req else ''
        email = req['email'] if 'email' in req else ''

        if nickname is None or len(nickname) < 2:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的姓名~~"
            return jsonify(resp)
        if email is None or len(email) < 2:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的邮箱~~"
            return jsonify(resp)

        # 更新数据库数据
        user_info = current_user
        user_info.nickname = nickname
        user_info.email = email
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_user.route("/reset-pwd", methods=["GET", "POST"])
@permission_required('reset_pwd')
def reset_pwd():
    if request.method == "GET":
        return optRender("user/reset_pwd.html", {'current': 'reset-pwd'})
    else:
        resp = {
            'code': 200,
            'msg': "修改成功",
            "data": {}
        }
        req = request.values
        old_password = req['old_password'] if 'old_password' in req else ''
        new_password = req['new_password'] if 'new_password' in req else ''

        user_info = current_user

        if old_password is None:
            resp['code'] = -1
            resp['msg'] = "请输入原密码~~"
            return jsonify(resp)
        if not user_info.check_password(genPwd(old_password, user_info.login_salt)):
            resp['code'] = -1
            resp['msg'] = "原密码错误~~"
            return jsonify(resp)
        if new_password is None or len(new_password) < 6:
            resp['code'] = -1
            resp['msg'] = "请输入不少于6位的新密码~~"
            return jsonify(resp)

        # 更新数据库数据
        user_info.login_pwd = user_info.set_password(genPwd(new_password, user_info.login_salt))
        db.session.add(user_info)
        db.session.commit()

        # 修改密码后设置cookie
        response = make_response(json.dumps(resp))
        login_user(user_info)
        return response


@route_user.route("/logout")
def logout():
    response = make_response(redirect("/user/login"))
    logout_user()
    return response
