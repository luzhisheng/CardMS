from flask import Blueprint, render_template

route_member = Blueprint("member_page", __name__)


@route_member.route("/index")
def index():
    return render_template('member/index.html')


@route_member.route("/comment")
def comment():
    return render_template('member/comment.html')
