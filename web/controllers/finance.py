from flask import Blueprint, request
from common.libs.Helper import optRender, paging, permission_required
from common.models.Model import MemberAddress, PayOrder, PayOrderItem, Card
from application import app, db
from sqlalchemy import func

route_finance = Blueprint('finance_page', __name__)


@route_finance.route("/index")
@permission_required("finance_index")
def index():
    query = PayOrder.query
    if request.values.get('status'):
        query = query.filter_by(status=request.values.get('status'))

    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    pay_list = query.order_by(PayOrder.id.desc()).all()[offset:limit]

    resp_data = {
        'list': pay_list,
        'pages': pages,
        'search_con': request.values,
        'status_mapping': PayOrder.status_mapping,
        'current': 'index'
    }
    return optRender("finance/index.html", resp_data)


@route_finance.route("/pay-info", methods=["GET"])
@permission_required("finance_index")
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
    return optRender('finance/pay_info.html', resp)


@route_finance.route("/account")
@permission_required("finance_account")
def account():
    query = PayOrder.query.filter_by(status=1)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    pay_order_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(20).all()

    # 查询总金额并添加 GROUP BY 子句
    stat_info = db.session.query(
        func.sum(PayOrder.total_price).label("total")
    ).filter(PayOrder.status == 1).group_by(PayOrder.status).first()

    app.logger.info(stat_info)
    resp_data = {
        'list': pay_order_list,
        'pages': pages,
        'total_money': stat_info[0] if stat_info[0] else 0.00,
        'current': 'account'
    }
    return optRender("finance/account.html", resp_data)
