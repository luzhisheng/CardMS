from werkzeug.utils import secure_filename
from application import app
from datetime import datetime
import os
import stat
import uuid


def getCurrentDate(format_str):
    return datetime.now().strftime(format_str)


class UploadService(object):

    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {"code": 200, "msg": "操作成功", "data": {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[1]
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['code'] = "不允许的扩展型文件"
            return resp
        root_path = app.root_path + config_upload['prefix_path']
        file_dir = getCurrentDate("%Y%m%d")
        save_dir = root_path + file_dir

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
        file.save("{0}/{1}".format(save_dir, file_name))

        resp['data'] = {
            'file_key': file_dir + "/" + file_name
        }

        return resp
