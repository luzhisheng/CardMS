from flask import Blueprint, request, jsonify
from web.controllers.helper import iPagination
from common.models.Model import Member, MemberComments, Cards
from web.controllers.helper import opt_render
from application import app, db

route_member = Blueprint('member_page', __name__)


def build_image_url(image_path):
    # 定义自定义过滤器
    return f'/static/upload/{image_path}'


@route_member.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query

    page_size = 20

    if 'mix_kw' in req:
        query = query.filter(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))

    if 'status' in req and int(req['status']) != 0:
        query = query.filter(Member.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': page_size,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * page_size
    list = query.order_by(Member.id.desc()).offset(offset).limit(page_size).all()

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = {
        "1": "正常",
        "-1": "已删除"
    }
    resp_data['current'] = 'index'
    return opt_render("member/index.html", resp_data)


@route_member.route("/ops", methods=["POST"])
def cat_ops():
    act = request.values.get('act')
    id = request.values.get('id')
    if act == "remove":
        resp = {
            'code': 200,
            'msg': "删除用户成功",
            "data": {}
        }
        user_info = Member.query.filter_by(id=id).first()
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
        user_info = Member.query.filter_by(id=id).first()
        user_info.status = 1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_member.route("/info", methods=["GET"])
def info():
    info = Member.query.filter_by(id=request.values.get('id')).first()
    resp = {"info": info, "current": "cat", "buildImageUrl": build_image_url}
    return opt_render('member/info.html', resp)


@route_member.route("/comment", methods=["GET"])
def comment():
    resp_data = {}
    req = request.args
    page = int(req['p']) if ('p' in req and req['p']) else 1

    # 查询评论并连接用户表
    query = db.session.query(MemberComments, Member, Cards).\
        join(Member, MemberComments.member_id == Member.id).\
        join(Cards, MemberComments.cards_id == Cards.id)

    page_params = {
        'total': query.count(),
        'page_size': 20,
        'page': page,
        'display': 10,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * 20

    comment_list = query.order_by(MemberComments.id.desc()).offset(offset).limit(20).all()

    data_list = []
    if comment_list:
        # 准备数据传递给模板
        for comment, member, card in comment_list:
            data_list.append({
                "avatar": member.avatar,
                "nickname": member.nickname,
                "cards_name": card.name,
                "content": comment.content,
                "score": comment.score
            })

    resp_data['list'] = data_list
    resp_data['pages'] = pages
    resp_data['current'] = 'comment'
    return opt_render("member/comment.html", resp_data)
