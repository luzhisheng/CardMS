SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/cardms"
SERVER_PORT = 5555
SERVER_HOST = "0.0.0.0"
SERVER_DEBUG = False
SQLALCHEMY_ECHO = False

# 图片上传目录
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_path_card': '/web/static/upload/card/',
    'prefix_path_member': '/web/static/upload/member/',
    'prefix_url': '/status/upload'
}
