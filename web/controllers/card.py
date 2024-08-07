from flask import Blueprint, request, jsonify
from common.libs.Helper import optRender, paging, isInteger, isValidIntegerStock, isValidPrice, permission_required
from common.models.Model import CardCat, Card, CardStockChangeLog, PayOrderItem, Member
from sqlalchemy import or_
from application import db

route_card = Blueprint("card_page", __name__)


@route_card.route("/index", methods=["GET", "POST"])
@permission_required("card_index")
def index():
    query = Card.query

    mix_kw = request.values.get('mix_kw')
    if mix_kw:
        # 搜索查询
        rule = or_(Card.name.ilike(f"%{mix_kw}%"), Card.summary.ilike(f"%{mix_kw}%"))
        query = query.filter(rule)

    cat_id = request.values.get('cat_id')
    if cat_id:
        # 分类查询
        query = query.filter_by(cat_id=cat_id)

    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    card_list = query.order_by(Card.id.desc()).all()[offset:limit]
    cats = CardCat.query.filter_by(status=1).all()
    # 构建类别映射字典
    cat_mapping = {cat.id: cat for cat in cats}
    resp = {
        'list': card_list,
        'pages': pages,
        'cat_mapping': cat_mapping,
        'search_con': request.values,
        "current": "index",
        'status_mapping': Card.status_mapping
    }
    return optRender('card/index.html', resp)


@route_card.route("/cat", methods=["GET"])
@permission_required("card_cat")
def cat():
    query = CardCat.query
    req = request.values

    if req.get('mix_kw'):
        # 搜索查询
        rule = CardCat.name.ilike(f"%{req.get('mix_kw')}%")
        query = query.filter(rule)

    if req.get('status'):
        # 状态查询
        query = query.filter_by(status=req.get('status'))

    count = query.count()
    # 获取分页数据
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    card_cat_list = query.order_by(CardCat.weight.desc()).all()[offset:limit]
    resp = {
        'list': card_cat_list,
        'pages': pages,
        'search_con': request.values,
        "current": "cat",
        'status_mapping': Card.status_mapping
    }
    return optRender('card/cat.html', resp)


@route_card.route("/set", methods=["GET", "POST"])
@permission_required("card_set")
def set():
    if request.method == "GET":
        if request.values.get('id'):
            cat_list = CardCat.query.filter_by(status=1).order_by(CardCat.weight.desc()).all()
            info = Card.query.filter_by(id=request.values.get('id')).first()
            rep = {"info": info, "current": "index", "cat_list": cat_list}
            return optRender('card/set.html', rep)
        else:
            cat_list = CardCat.query.filter_by(status=1).order_by(CardCat.weight.desc()).all()
            rep = {"info": "", "current": "index", "cat_list": cat_list}
            return optRender('card/set.html', rep)
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
        if price is None or not isValidPrice(price):
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
        if stock is None or not isValidIntegerStock(stock):
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
            info = Card.query.filter_by(id=int(request.values.get('id'))).first()
            resp['msg'] = "修改卡券成功"
        else:
            # 新增数据
            info = Card()
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


@route_card.route("/cat-set", methods=["GET", "POST"])
@permission_required("card_cat_set")
def cat_set():
    if request.method == "GET":
        if request.values.get('id'):
            info = CardCat.query.filter_by(id=request.values.get('id')).first()
            rep = {"info": info, "current": "cat"}
            return optRender('card/cat_set.html', rep)
        else:
            rep = {"info": "", "current": "cat"}
            return optRender('card/cat_set.html', rep)
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
        if weight is None or len(weight) < 1 or not isInteger(weight):
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的权重~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            info = CardCat.query.filter_by(id=int(request.values.get('id'))).first()
            resp['msg'] = "修改用户成功"
        else:
            # 新增数据
            info = CardCat()
        info.name = name
        info.weight = weight
        db.session.add(info)
        db.session.commit()
        return jsonify(resp)


@route_card.route("/cat-ops", methods=["POST"])
@permission_required("card_cat_ops")
def cat_ops():
    act = request.values.get('act')
    id = request.values.get('id')
    if act == "remove":
        resp = {
            'code': 200,
            'msg': "删除用户成功",
            "data": {}
        }
        user_info = CardCat.query.filter_by(id=id).first()
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
        user_info = CardCat.query.filter_by(id=id).first()
        user_info.status = 1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_card.route("/ops", methods=["POST"])
@permission_required("card_ops")
def ops():
    act = request.values.get('act')
    id = request.values.get('id')
    if act == "remove":
        resp = {
            'code': 200,
            'msg': "删除卡券成功",
            "data": {}
        }
        info = Card.query.filter_by(id=id).first()
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
        info = Card.query.filter_by(id=id).first()
        info.status = 1
        db.session.add(info)
        db.session.commit()
        return jsonify(resp)


@route_card.route("/info", methods=["GET"])
@permission_required("card_index")
def info():
    req_id = request.values.get('id')
    info = Card.query.filter_by(id=req_id).first()
    stock_change_list = CardStockChangeLog.get_logs(card_id=req_id)

    # 使用关联查询获取 PayOrderItem 及对应的 Member 信息
    pay_order_items = db.session.query(PayOrderItem, Member).join(Member, PayOrderItem.member_id == Member.id).filter(
        PayOrderItem.card_id == req_id).all()

    # 将查询结果整理为需要的格式
    pay_order_item_list = [{
        "pay_order_item": item[0],
        "member": item[1]
    } for item in pay_order_items]

    resp = {
        "info": info,
        "stock_change_list": stock_change_list,
        "pay_order_item_list": pay_order_item_list,
        "current": "index"
    }
    return optRender('card/info.html', resp)
