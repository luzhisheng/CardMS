from flask import Blueprint, request
from common.libs.Helper import getFormatDate, paging, getDictFilterField, selectFilterObj, optRender
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
    default_date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    req = request.values
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    stat_daily_site_list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(20).all()
    resp_data = {
        'list': stat_daily_site_list,
        'pages': pages,
        'current': 'index',
        'search_con': {
            'date_from': date_from,
            'date_to': date_to
        }
    }
    return optRender("stat/index.html", resp_data)


@route_stat.route("/cards")
def cards():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    req = request.values
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailyCard.query.filter(StatDailyCard.date >= date_from).filter(StatDailyCard.date <= date_to)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    stat_daily_card_list = query.order_by(StatDailyCard.id.desc()).offset(offset).limit(20).all()
    date_list = []
    if stat_daily_card_list:
        card_map = getDictFilterField(Card, Card.id, "id", selectFilterObj(stat_daily_card_list, "card_id"))
        for item in stat_daily_card_list:
            tmp_food_info = card_map[item.card_id] if item.card_id in card_map else {}
            tmp_data = {
                "date": item.date,
                "total_count": item.total_count,
                "total_pay_money": item.total_pay_money,
                'food_info': tmp_food_info
            }
            date_list.append(tmp_data)
    resp_data = {
        'list': date_list,
        'pages': pages,
        'current': 'cards',
        'search_con': {
            'date_from': date_from,
            'date_to': date_to
        }
    }
    return optRender("stat/cards.html", resp_data)


@route_stat.route("/member")
def memebr():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    req = request.values
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailyMember.query.filter(StatDailyMember.date >= date_from) \
        .filter(StatDailyMember.date <= date_to)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    stat_daily_member_list = query.order_by(StatDailyMember.id.desc()).offset(offset).limit(20).all()
    date_list = []
    if stat_daily_member_list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(stat_daily_member_list, "member_id"))
        for item in stat_daily_member_list:
            tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
            tmp_data = {
                "date": item.date,
                "total_pay_money": item.total_pay_money,
                "total_shared_count": item.total_shared_count,
                'member_info': tmp_member_info
            }
            date_list.append(tmp_data)
    resp_data = {
        'list': date_list,
        'pages': pages,
        'current': 'member',
        'search_con': {
            'date_from': date_from,
            'date_to': date_to
        }
    }
    return optRender("stat/member.html", resp_data)


@route_stat.route("/share")
def share():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    req = request.values
    date_from = req['date_from'] if req.get('date_from') else default_date_from
    date_to = req['date_to'] if req.get('date_to') else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from).filter(StatDailySite.date <= date_to)

    # 获取分页数据
    count = query.count()
    p = request.values.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    stat_daily_site_list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(10).all()
    resp_data = {
        'list': stat_daily_site_list,
        'pages': pages,
        'current': 'share',
        'search_con': {
            'date_from': date_from,
            'date_to': date_to
        }
    }
    return optRender("stat/share.html", resp_data)
