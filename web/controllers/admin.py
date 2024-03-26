from flask import Blueprint
from web.controllers.helper import opt_render

route_admin = Blueprint("admin_page", __name__)


@route_admin.route("/")
def index():
    return opt_render('admin/index.html')
