from flask import Blueprint, request, jsonify
from flask import make_response, redirect, g
from web.controllers.helper import opt_render, gen_pwd, gene_auth_code
from application import db
import json
from common.models.Model import User


route_user = Blueprint("user_page", __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return opt_render("user/login.html")
    else:
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

        # 密码加密
        if user_info.login_pwd != gen_pwd(login_pwd, user_info.login_salt):
            resp['code'] = -1
            resp['msg'] = "请输入正确的用户名/密码-4"
            return jsonify(resp)

        # 设置cookie
        response = make_response(json.dumps(resp))
        response.set_cookie("file_server", f"{gene_auth_code(user_info)}#{user_info.uid}")
        return response


@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return opt_render("user/edit.html", {'current': 'edit'})
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
        user_info = g.current_user
        user_info.nickname = nickname
        user_info.email = email
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_user.route("/reset-pwd", methods=["GET", "POST"])
def reset_pwd():
    if request.method == "GET":
        return opt_render("user/reset_pwd.html", {'current': 'reset-pwd'})
    else:
        resp = {
            'code': 200,
            'msg': "修改成功",
            "data": {}
        }
        req = request.values
        old_password = req['old_password'] if 'old_password' in req else ''
        new_password = req['new_password'] if 'new_password' in req else ''

        user_info = g.current_user

        if old_password is None:
            resp['code'] = -1
            resp['msg'] = "请输入原密码~~"
            return jsonify(resp)
        if gen_pwd(old_password, user_info.login_salt) != user_info.login_pwd:
            resp['code'] = -1
            resp['msg'] = "原密码错误~~"
            return jsonify(resp)
        if new_password is None or len(new_password) < 6:
            resp['code'] = -1
            resp['msg'] = "请输入不少于6位的新密码~~"
            return jsonify(resp)

        # 更新数据库数据
        user_info.login_pwd = gen_pwd(new_password, user_info.login_salt)
        db.session.add(user_info)
        db.session.commit()

        # 修改密码后设置cookie
        response = make_response(json.dumps(resp))
        response.set_cookie("file_server", f"{gene_auth_code(user_info)}#{user_info.uid}")
        return response


@route_user.route("/logout")
def logout():
    response = make_response(redirect("/user/login"))
    response.delete_cookie("file_server")
    return response
