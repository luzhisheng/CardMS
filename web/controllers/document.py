from flask import Blueprint, render_template

route_document = Blueprint("document_page", __name__)


@route_document.route("/index")
def index():
    return render_template('document/index.html')


@route_document.route("/cat")
def cat():
    return render_template('document/cat.html')
