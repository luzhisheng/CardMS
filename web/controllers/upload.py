from flask import Blueprint, render_template, request, jsonify
from common.libs.UploadService import UploadService

route_upload = Blueprint("upload_page", __name__)


@route_upload.route("/ueditor", methods=["GET", "POST"])
def ueditor():
    return "upload"


@route_upload.route("/pic_card", methods=["POST"])
def pic_card():
    file_target = request.files
    up_file = file_target['pic'] if 'pic' in file_target else None
    callback_target = 'window.parent.upload'
    if up_file is None:
        msg = '上传失败'
        return f"<script type='text/javascript'>{callback_target}.error('{msg}')</script>"
    ret = UploadService.uploadByFile(up_file, "card")
    if ret['code'] != 200:
        msg = '上传失败' + ret['msg']
        return f"<script type='text/javascript'>{callback_target}.error('{msg}')</script>"
    msg = ret['data']['file_key']
    return f"<script type='text/javascript'>{callback_target}.success('{msg}')</script>"


@route_upload.route("/pic_member", methods=["POST"])
def pic_member():
    file_target = request.files
    up_file = file_target['pic'] if 'pic' in file_target else None
    callback_target = 'window.parent.upload'
    if up_file is None:
        msg = '上传失败'
        return f"<script type='text/javascript'>{callback_target}.error('{msg}')</script>"
    ret = UploadService.uploadByFile(up_file, "member")
    if ret['code'] != 200:
        msg = '上传失败' + ret['msg']
        return f"<script type='text/javascript'>{callback_target}.error('{msg}')</script>"
    msg = ret['data']['file_key']
    return f"<script type='text/javascript'>{callback_target}.success('{msg}')</script>"