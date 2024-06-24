from application import app, db
from flask import Blueprint
from common.libs.Helper import ops_render
from common.libs.Helper import getFormatDate
from common.models.Model import StatDailySite
import datetime

route_admin = Blueprint("admin_page", __name__)


@route_admin.route("/")
def index():
    """
    仪表盘统计数据
    :return:
    """
    resp_data = {
        'data': {
            'finance': {
                'today': 0,
                'month': 0
            },
            'member': {
                'today': 0,
                'month': 0
            },
            'order': {
                'today': 0,
                'month': 0
            },
            'shared': {
                'today': 0,
                'month': 0
            },
        }
    }

    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    date_to = getFormatDate(date=now, format="%Y-%m-%d")

    list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
        .all()
    data = resp_data['data']
    if list:

        for item in list:
            data['finance']['month'] += item.total_pay_money
            data['member']['month'] = item.total_member_count
            data['order']['month'] += item.total_order_count
            data['shared']['month'] += item.total_shared_count
            if getFormatDate(date=item.date, format="%Y-%m-%d") == date_to:
                data['finance']['today'] = item.total_pay_money
                data['member']['today'] = item.total_member_count
                data['order']['today'] = item.total_order_count
                data['shared']['today'] = item.total_shared_count

    return ops_render("admin/index.html", resp_data)
