from flask import Blueprint, request
from web.controllers.helper import opt_render
from common.models.Model import MemberAddress, PayOrder, PayOrderItem, Card
from application import app, db
from web.controllers.helper import iPagination
from sqlalchemy import func

route_finance = Blueprint('finance_page', __name__)


@route_finance.route("/index")
def index():
    count = PayOrder.query.count()
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
        "url": '/card/index?'
    }
    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page_size * page

    query = PayOrder.query
    status = request.values.get('status')
    if status:
        query = query.filter_by(status=status)
    pay_list = query.order_by(PayOrder.id.desc()).all()[offset:limit]

    resp_data = {
        'list': pay_list,
        'pages': pages,
        'search_con': request.values,
        'pay_status_mapping': PayOrder.pay_status_display_mapping,
        'current': 'index'
    }
    return opt_render("finance/index.html", resp_data)


@route_finance.route("/pay-info", methods=["GET"])
def pay_info():

    pay_info_id = request.values.get('id')

    # 查询订单并连接卡券表和价格表
    pay_order = PayOrder.query.filter(PayOrder.id == pay_info_id).first()
    member = MemberAddress.query.filter_by(id=pay_order.express_address_id).first()

    # 2. 提取出所有 card_id
    query = db.session.query(
        PayOrderItem.quantity,
        PayOrderItem.price,
        PayOrderItem.note,
        Card.name.label("name")
    ).join(Card, PayOrderItem.card_id == Card.id)
    results = query.filter(PayOrderItem.pay_order_id == pay_info_id).all()

    # 准备数据传递给模板
    resp = {
        "pay_order": pay_order,
        "member": member,
        "pay_order_item": results
    }
    return opt_render('finance/pay_info.html', resp)


@route_finance.route("/account")
def account():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = PayOrder.query.filter_by(status=1)

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20
    list = query.order_by(PayOrder.id.desc()).offset(offset).limit(20).all()

    # 查询总金额并添加 GROUP BY 子句
    stat_info = db.session.query(
        func.sum(PayOrder.total_price).label("total")
    ).filter(PayOrder.status == 1).group_by(PayOrder.status).first()

    app.logger.info(stat_info)
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['total_money'] = stat_info[0] if stat_info[0] else 0.00
    resp_data['current'] = 'account'
    return opt_render("finance/account.html", resp_data)
