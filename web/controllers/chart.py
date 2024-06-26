from flask import Blueprint, jsonify
from common.libs.Helper import getFormatDate
from common.models.Model import StatDailySite
from common.models.Model import StatDailyMember
from common.models.Model import StatDailyCard
import datetime

route_chart = Blueprint('chart_page', __name__)


@route_chart.route("/dashboard")
def dashboard():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
        .all()

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "categories": [],
        "series": [
            {
                "name": "会员总数",
                "data": []
            },
            {
                "name": "订单总数",
                "data": []
            },
        ]
    }

    if list:
        for item in list:
            data['categories'].append(getFormatDate(date=item.date, date_format="%Y-%m-%d"))
            data['series'][0]['data'].append(item.total_member_count)
            data['series'][1]['data'].append(item.total_order_count)

    resp['data'] = data
    return jsonify(resp)


@route_chart.route("/finance")
def finance():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
        .all()

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "categories": [],
        "series": [
            {
                "name": "日营收报表",
                "data": []
            }
        ]
    }

    if list:
        for item in list:
            data['categories'].append(getFormatDate(date=item.date, date_format="%Y-%m-%d"))
            data['series'][0]['data'].append(float(item.total_pay_money))

    resp['data'] = data
    return jsonify(resp)


@route_chart.route("/share")
def share():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
        .all()

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "categories": [],
        "series": [
            {
                "name": "日分享",
                "data": []
            }
        ]
    }

    if list:
        for item in list:
            data['categories'].append(getFormatDate(date=item.date, date_format="%Y-%m-%d"))
            data['series'][0]['data'].append(item.total_shared_count)

    resp['data'] = data
    return jsonify(resp)


@route_chart.route("/member")
def member():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    list = StatDailyMember.query.filter(StatDailyMember.date >= date_from) \
        .filter(StatDailyMember.date <= date_to).order_by(StatDailyMember.id.asc()) \
        .all()

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "categories": [],
        "series": [
            {
                "name": "日会员消费",
                "data": []
            }
        ]
    }

    if list:
        for item in list:
            data['categories'].append(getFormatDate(date=item.date, date_format="%Y-%m-%d"))
            data['series'][0]['data'].append(item.total_shared_count)

    resp['data'] = data
    return jsonify(resp)


@route_chart.route("/card")
def card():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30days, date_format="%Y-%m-%d")
    date_to = getFormatDate(date=now, date_format="%Y-%m-%d")

    list = StatDailyCard.query.filter(StatDailyCard.date >= date_from) \
        .filter(StatDailyCard.date <= date_to).order_by(StatDailyCard.id.asc()) \
        .all()

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "categories": [],
        "series": [
            {
                "name": "日售卖",
                "data": []
            }
        ]
    }

    if list:
        for item in list:
            data['categories'].append(getFormatDate(date=item.date, date_format="%Y-%m-%d"))
            data['series'][0]['data'].append(item.total_shared_count)

    resp['data'] = data
    return jsonify(resp)

