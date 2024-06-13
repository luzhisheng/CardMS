from flask import Blueprint, render_template, request, jsonify
from web.controllers.helper import opt_render
from common.models.Model import CardsCat, Cards
from web.controllers.helper import iPagination
from sqlalchemy import or_
from application import db
import re

route_cards = Blueprint("cards_page", __name__)


def is_valid_price(price_str):
    # 使用正则表达式检查价格格式是否正确
    pattern = r'^\d+(\.\d{1,2})?$'
    return re.match(pattern, price_str) is not None


def is_valid_integer_stock(stock_str):
    # 检查价格是否为有效的整数
    try:
        stock = int(stock_str)
        return True
    except ValueError:
        return False


def build_image_url(image_path):
    # 定义自定义过滤器
    return f'/static/upload/{image_path}'


@route_cards.route("/index", methods=["GET", "POST"])
def index():
    count = Cards.query.count()
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

    query = Cards.query

    mix_kw = request.values.get('mix_kw')
    if mix_kw:
        # 搜索查询
        rule = or_(Cards.name.ilike(f"%{mix_kw}%"), Cards.summary.ilike(f"%{mix_kw}%"))
        query = query.filter(rule)

    cat_id = request.values.get('cat_id')
    if cat_id:
        # 分类查询
        query = query.filter_by(cat_id=cat_id)

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    cards_list = query.order_by(Cards.id.desc()).all()[offset:limit]
    cats = CardsCat.query.filter_by(status=1).all()
    # 构建类别映射字典
    cat_mapping = {cat.id: cat for cat in cats}
    resp = {
        'list': cards_list,
        'pages': pages,
        'cat_mapping': cat_mapping,
        'search_con': request.values,
        "current": "index",
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
        "current": "cat",
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
            cat_list = CardsCat.query.filter_by(status=1).order_by(CardsCat.weight.desc()).all()
            info = Cards.query.filter_by(id=request.values.get('id')).first()
            rep = {"info": info, "current": "index", "buildImageUrl": build_image_url, "cat_list": cat_list}
            return opt_render('cards/set.html', rep)
        else:
            cat_list = CardsCat.query.filter_by(status=1).order_by(CardsCat.weight.desc()).all()
            rep = {"info": "", "current": "index", "cat_list": cat_list}
            return opt_render('cards/set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增卡券成功",
            "data": {}
        }
        cat_id = request.values.get('cat_id')
        if cat_id is None or int(cat_id) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的分类~~"
            return jsonify(resp)

        name = request.values.get('name')
        if name is None or len(name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的名称~~"
            return jsonify(resp)

        price = request.values.get('price')
        if price is None or not is_valid_price(price):
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的价格~~"
            return jsonify(resp)

        main_image = request.values.get('main_image')
        if main_image is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的封面图~~"
            return jsonify(resp)

        summary = request.values.get('summary')
        if summary is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的描述~~"
            return jsonify(resp)

        stock = request.values.get('stock')
        if stock is None or not is_valid_integer_stock(stock):
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的库存~~"
            return jsonify(resp)

        tags = request.values.get('tags')
        if tags is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的标签~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            info = Cards.query.filter_by(id=int(request.values.get('id'))).first()
            resp['msg'] = "修改卡券成功"
        else:
            # 新增数据
            info = Cards()
        info.cat_id = cat_id
        info.name = name
        info.price = price
        info.main_image = main_image
        info.summary = summary
        info.stock = stock
        info.tags = tags
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


@route_cards.route("/ops", methods=["POST"])
def ops():
    act = request.values.get('act')
    id = request.values.get('id')
    if act == "remove":
        resp = {
            'code': 200,
            'msg': "删除卡券成功",
            "data": {}
        }
        info = Cards.query.filter_by(id=id).first()
        info.status = -1
        db.session.add(info)
        db.session.commit()
        return jsonify(resp)
    else:
        resp = {
            'code': 200,
            'msg': "恢复卡券成功",
            "data": {}
        }
        info = Cards.query.filter_by(id=id).first()
        info.status = 1
        db.session.add(info)
        db.session.commit()
        return jsonify(resp)


@route_cards.route("/info", methods=["GET"])
def info():
    info = Cards.query.filter_by(id=request.values.get('id')).first()
    resp = {"info": info, "current": "cat", "buildImageUrl": build_image_url}
    return opt_render('cards/info.html', resp)
