from application import app
from common.models.Model import User
from flask import request, g
from flask import redirect
import hashlib
import base64


def gene_auth_code(user_info):
    m = hashlib.md5()
    str = f"{user_info.login_name}-{user_info.login_salt}-{user_info.login_pwd}-{user_info.uid}"
    base64.encodebytes(str.encode('utf-8'))
    m.update(str.encode("utf-8"))
    return m.hexdigest()


# @app.before_request是一个装饰器，用于注册一个在每个请求之前执行的函数。
@app.before_request
def before_request():
    path = request.path
    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info
    # 处理一些不需要登陆就可以访问的地址
    if "/static/" in path:
        return
    if path == "/user/login" and user_info:
        return redirect("/admin")
    if path == "/user/login" and not user_info:
        return
    if not user_info:
        return redirect("/user/login")
    return


# 判断用户是否登陆
def check_login():
    cookies = request.cookies
    auth_cookie = cookies.get("file_server") if cookies.get("file_server") else ''
    if auth_cookie is None:
        return False
    else:
        auth_info = auth_cookie.split("#")
        if len(auth_info) != 2:
            return False
        try:
            user_info = User.query.filter_by(uid=auth_info[1]).first()
        except Exception:
            return False

        if user_info is None:
            return False

        if auth_info[0] != gene_auth_code(user_info):
            return False

        if user_info.status != 1:
            return False

        return user_info
