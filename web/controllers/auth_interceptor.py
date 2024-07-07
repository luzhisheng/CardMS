from application import app, db, login_manager
from common.models.Model import User, SysLog
from flask import request, g
from flask_login import current_user
from urllib.parse import urlparse
import time


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

        if current_user.is_authenticated:
            log = SysLog(
                nickname=current_user.nickname,
                account_id=current_user.uid,
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


@login_manager.user_loader
def load_user(user_id):
    """
    定义用户加载函数
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))
