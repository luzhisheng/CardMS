from flask import Blueprint, request
from web.controllers.helper import opt_render
from common.models.Model import Member, Cards, PayOrder, PayOrderItem
from application import app, db
from web.controllers.helper import iPagination
from sqlalchemy import func

route_finance = Blueprint('finance_page', __name__)


@route_finance.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    # 查询订单并连接卡券表和价格表
    query = db.session.query(PayOrderItem, PayOrder, Cards) \
        .join(PayOrder, PayOrderItem.pay_order_id == PayOrder.id) \
        .join(Cards, PayOrderItem.cards_id == Cards.id)

    if 'status' in req and int(req['status']) >= -8 and int(req['status']) != -1:
        query = query.filter(PayOrder.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20
    pay_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(20).all()
    data_list = []

    if pay_list:
        # 准备数据传递给模板
        for pay_order_item, pay_order, cards in pay_list:
            tmp_data = {
                "id": pay_order.id,
                "name": cards.name,
                "status_desc": pay_order.status_desc,
                "order_number": pay_order.order_number,
                "price": pay_order_item.price,
                "pay_time": pay_order.pay_time,
                "created_time": pay_order.pay_time
            }
            data_list.append(tmp_data)

    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['pay_status_mapping'] = {
        "1": "已支付",
        "-8": "待支付",
        "0": "已关闭"
    }
    resp_data['current'] = 'index'

    return opt_render("finance/index.html", resp_data)


@route_finance.route("/pay-info", methods=["GET"])
def pay_info():
    # 查询订单并连接卡券表和价格表
    info = db.session.query(PayOrder, Member) \
        .join(Member, PayOrder.member_id == Member.id) \
        .filter(PayOrder.id == request.values.get('id')).first()

    if info:
        # 准备数据传递给模板
        resp = {
            "pay_order_info": info.PayOrder,
            "member_info": info.Member,
            "address_info": info.Member,
            "pay_order_items": ""
        }
    else:
        resp = {
            "pay_order_info": "",
            "member_info": "",
            "address_info": "",
            "pay_order_items": ""
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
