SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/file_server"
SERVER_PORT = 5555
SERVER_HOST = "0.0.0.0"
SERVER_DEBUG = False
SQLALCHEMY_ECHO = False
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/status/upload'
}
