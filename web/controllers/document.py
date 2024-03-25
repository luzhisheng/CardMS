from flask import Blueprint, render_template

route_document = Blueprint("document_page", __name__)


@route_document.route("/index")
def index():
    return render_template('document/index.html')


@route_document.route("/cat")
def cat():
    return render_template('document/cat.html')


@route_document.route("/set")
def set():
    return render_template('document/set.html')


@route_document.route("/cat-set")
def cat_set():
    return render_template('document/cat_set.html')
