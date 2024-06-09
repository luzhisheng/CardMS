from flask import Blueprint, render_template, request, jsonify
from web.controllers.helper import opt_render
from common.models.Model import CardsCat
from web.controllers.helper import iPagination
from sqlalchemy import or_
from application import db

route_cards = Blueprint("cards_page", __name__)


@route_cards.route("/index", methods=["GET", "POST"])
def index():
    user_count = CardsCat.query.count()
    p = request.values.get('p')

    page_size = 20
    if not p:
        page = 1
    else:
        page = int(p)

    params = {
        "total": user_count,  # 总数
        "page_size": page_size,  # 每页的数量
        "page": int(page),  # 第几页
        "display": 10,
        "url": '/cards/index?'
    }
    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page_size * page

    query = CardsCat.query

    mix_kw = request.values.get('mix_kw')
    if mix_kw:
        # 搜索查询
        rule = or_(CardsCat.nickname.ilike(f"%{mix_kw}%"), CardsCat.mobile.ilike(f"%{mix_kw}%"))
        query = query.filter(rule)

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    user_list = query.order_by(CardsCat.id.desc()).all()[offset:limit]
    resp = {
        'user_list': user_list,
        'pages': pages,
        'search_con': request.values,
        'status_mapping': {
            "1": "正常",
            "-1": "已删除"
        }
    }
    return opt_render('cards/index.html', resp)


@route_cards.route("/cat", methods=["GET"])
def cat():
    count = CardsCat.query.count()
    p = request.values.get('p')

    page_size = 20
    if not p:
        page = 1
    else:
        page = int(p)

    params = {
        "total": count,  # 总数
        "page_size": page_size,  # 每页的数量
        "page": int(page),  # 第几页
        "display": 10,
        "url": '/cards/index?'
    }
    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page_size * page

    query = CardsCat.query

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    cards_cat_list = query.order_by(CardsCat.weight.desc()).all()[offset:limit]
    resp = {
        'list': cards_cat_list,
        'pages': pages,
        'search_con': request.values,
        'status_mapping': {
            "1": "正常",
            "-1": "已删除"
        }
    }
    return opt_render('cards/cat.html', resp)


@route_cards.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        if request.values.get('id'):
            info = CardsCat.query.filter_by(id=request.values.get('id')).first()
            rep = {"info": info, "current": "cat"}
            return opt_render('cards/set.html', rep)
        else:
            rep = {"info": "", "current": "cat"}
            return opt_render('cards/set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增卡券成功",
            "data": {}
        }
        name = request.values.get('name')
        if name is None or len(name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的分类~~"
            return jsonify(resp)

        weight = request.values.get('weight')
        if weight is None or len(weight) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的权重~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            info = CardsCat.query.filter_by(id=int(request.values.get('id'))).first()
            resp['msg'] = "修改卡券成功"
        else:
            # 新增数据
            info = CardsCat()
        info.name = name
        info.weight = weight
        db.session.add(info)
        db.session.commit()
        return jsonify(resp)


@route_cards.route("/cat-set", methods=["GET", "POST"])
def cat_set():
    if request.method == "GET":
        if request.values.get('id'):
            info = CardsCat.query.filter_by(id=request.values.get('id')).first()
            rep = {"info": info, "current": "cat"}
            return opt_render('cards/cat_set.html', rep)
        else:
            rep = {"info": "", "current": "cat"}
            return opt_render('cards/cat_set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增分类成功",
            "data": {}
        }
        name = request.values.get('name')
        if name is None or len(name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的分类~~"
            return jsonify(resp)

        weight = request.values.get('weight')
        if weight is None or len(weight) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的权重~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            info = CardsCat.query.filter_by(id=int(request.values.get('id'))).first()
            resp['msg'] = "修改用户成功"
        else:
            # 新增数据
            info = CardsCat()
        info.name = name
        info.weight = weight
        db.session.add(info)
        db.session.commit()
        return jsonify(resp)


@route_cards.route("/cat-ops", methods=["POST"])
def cat_ops():
    act = request.values.get('act')
    id = request.values.get('id')
    if act == "remove":
        resp = {
            'code': 200,
            'msg': "删除用户成功",
            "data": {}
        }
        user_info = CardsCat.query.filter_by(id=id).first()
        user_info.status = -1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)
    else:
        resp = {
            'code': 200,
            'msg': "恢复用户成功",
            "data": {}
        }
        user_info = CardsCat.query.filter_by(id=id).first()
        user_info.status = 1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)
