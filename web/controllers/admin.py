from flask import Blueprint, render_template

route_admin = Blueprint("admin_page", __name__)


@route_admin.route("/")
def index():
    return render_template('admin/index.html')
