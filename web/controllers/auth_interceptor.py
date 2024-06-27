from application import app, db
from common.models.Model import User, SysLog
from flask import request, g
from flask import redirect
from urllib.parse import urlparse
import hashlib
import base64
import time


def gene_auth_code(user_info):
    m = hashlib.md5()
    str = f"{user_info.login_name}-{user_info.login_salt}-{user_info.login_pwd}-{user_info.uid}"
    base64.encodebytes(str.encode('utf-8'))
    m.update(str.encode("utf-8"))
    return m.hexdigest()


@app.after_request
def after_request_logging(response):
    """
    函数在请求结束时计算请求持续时间，并将日志信息保存到数据库中
    :return:
    """ 
    duration = time.time() - g.start_time
    url_path = urlparse(request.url).path
    operation_key_list = list(SysLog.operation_mapping.keys())
    if url_path in operation_key_list:

        params = {}
        if request.method == 'GET':
            params = request.args.to_dict()  # 获取查询参数
        elif request.method == 'POST':
            if request.is_json:
                params = request.get_json()  # 获取JSON数据
            else:
                params = request.form.to_dict()  # 获取表单数据

        log = SysLog(
            nickname=g.current_user.nickname,
            account_id=g.current_user.uid,
            account_type=1,
            operation=url_path,
            method=request.method,
            params=str(params),
            time=int(duration * 1000),
            ip=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    return response


@app.before_request
def before_request():
    """
    函数在请求开始时记录开始时间
    :return:
    """
    g.start_time = time.time()
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
