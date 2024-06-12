from flask import Blueprint, render_template, request, jsonify
from common.libs.UploadService import UploadService

route_upload = Blueprint("upload_page", __name__)


@route_upload.route("/ueditor", methods=["GET", "POST"])
def ueditor():
    return "upload"


@route_upload.route("/pic", methods=["GET", "POST"])
def ueditor_pic():
    file_target = request.files
    up_file = file_target['pic'] if 'pic' in file_target else None
    callback_target = 'window.parent.upload'
    if up_file is None:
        msg = '上传失败'
        return f"<script type='text/javascript'>{callback_target}.error('{msg}')</script>"
    ret = UploadService.uploadByFile(up_file)
    if ret['code'] != 200:
        msg = '上传失败' + ret['msg']
        return f"<script type='text/javascript'>{callback_target}.error('{msg}')</script>"
    msg = ret['data']['file_key']
    return f"<script type='text/javascript'>{callback_target}.success('{msg}')</script>"
