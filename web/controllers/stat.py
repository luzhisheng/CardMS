from flask import Blueprint, request
from web.controllers.helper import opt_render
from application import app
from common.libs.Helper import getFormatDate, iPagination, getDictFilterField, selectFilterObj
from common.models.Model import StatDailySite
from common.models.Model import StatDailyCards
from common.models.Model import StatDailyMember
from common.models.Model import Member
import datetime

route_stat = Blueprint("stat_page", __name__)


@route_stat.route("/index")
def index():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20

    list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(20).all()
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'index'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return opt_render("stat/index.html", resp_data)
