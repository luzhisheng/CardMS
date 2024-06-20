from flask import Blueprint, request
from web.controllers.helper import opt_render
from application import app
from common.libs.Helper import getFormatDate, iPagination, getDictFilterField, selectFilterObj
from common.models.Model import StatDailySite
from common.models.Model import StatDailyCard
from common.models.Model import StatDailyMember
from common.models.Model import Member
from common.models.Model import Card
import datetime

route_stat = Blueprint("stat_page", __name__)


@route_stat.route("/index", methods=["GET"])
def index():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)

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


@route_stat.route("/cards")
def cards():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailyCard.query.filter(StatDailyCard.date >= date_from).filter(StatDailyCard.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20

    list = query.order_by(StatDailyCard.id.desc()).offset(offset).limit(20).all()
    date_list = []
    if list:
        food_map = getDictFilterField(Card, Card.id, "id", selectFilterObj(list, "food_id"))
        for item in list:
            tmp_food_info = food_map[item.cards_id] if item.cards_id in food_map else {}
            tmp_data = {
                "date": item.date,
                "total_count": item.total_count,
                "total_pay_money": item.total_pay_money,
                'food_info': tmp_food_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'cards'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return opt_render("stat/cards.html", resp_data)


@route_stat.route("/member")
def memebr():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailyMember.query.filter(StatDailyMember.date >= date_from) \
        .filter(StatDailyMember.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20

    list = query.order_by(StatDailyMember.id.desc()).offset(offset).limit(20).all()
    date_list = []
    if list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
        for item in list:
            tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
            tmp_data = {
                "date": item.date,
                "total_pay_money": item.total_pay_money,
                "total_shared_count": item.total_shared_count,
                'member_info': tmp_member_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'member'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return opt_render("stat/member.html", resp_data)


@route_stat.route("/share")
def share():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20

    list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(10).all()
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'share'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return opt_render("stat/share.html", resp_data)
