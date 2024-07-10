from flask import Blueprint, request, jsonify
from common.libs.Helper import optRender, paging, permission_required
from common.models.Model import Member, MemberComments, Card
from application import db

route_member = Blueprint('member_page', __name__)


@route_member.route("/index")
@permission_required("member_index")
def index():
    req = request.values
    query = Member.query

    if 'mix_kw' in req:
        query = query.filter(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))

    if 'status' in req and int(req['status']) != 0:
        query = query.filter(Member.status == int(req['status']))

    # 获取分页数据
    count = query.count()
    p = req.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    member_list = query.order_by(Member.id.desc()).offset(offset).limit(page_size).all()
    resp_data = {
        'list': member_list,
        'pages': pages,
        'search_con': req,
        'status_mapping': Member.status_mapping,
        'current': 'index'
    }
    return optRender("member/index.html", resp_data)


@route_member.route("/set", methods=["GET", "POST"])
@permission_required("member_set")
def set():
    if request.method == "GET":
        rep = {"info": ""}
        if request.values.get('id'):
            member_info = Member.query.filter_by(id=request.values.get('id')).first()
            rep['info'] = member_info
        return optRender('member/set.html', rep)
    elif request.method == "POST":
        resp = {
            'code': 200,
            'msg': "新增用户成功",
            "data": {}
        }

        nickname = request.values.get('nickname')
        if nickname is None or len(nickname) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的会员名称~~"
            return jsonify(resp)
        mobile = request.values.get('mobile')
        if mobile is None or len(mobile) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的手机号码~~"
            return jsonify(resp)
        avatar = request.values.get('avatar')
        if avatar is None:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的头像~~"
            return jsonify(resp)

        if request.values.get('id'):
            # 修改数据
            member_info = Member.query.filter_by(id=request.values.get('id')).first()
            resp['msg'] = "修改用户成功"
        else:
            # 新增数据
            member_info = Member
        member_info.nickname = nickname
        member_info.mobile = mobile
        member_info.avatar = avatar
        db.session.add(member_info)
        db.session.commit()
        return jsonify(resp)


@route_member.route("/ops", methods=["POST"])
@permission_required("member_ops")
def cat_ops():
    req = request.values
    if req.get('act') == "remove":
        resp = {
            'code': 200,
            'msg': "删除用户成功",
            "data": {}
        }
        user_info = Member.query.filter_by(id=req.get('id')).first()
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
        user_info = Member.query.filter_by(id=req.get('id')).first()
        user_info.status = 1
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)


@route_member.route("/info", methods=["GET"])
@permission_required("member_index")
def info():
    info = Member.query.filter_by(id=request.values.get('id')).first()
    resp = {"info": info}
    return optRender('member/info.html', resp)


@route_member.route("/comment", methods=["GET"])
@permission_required("member_comment")
def comment():
    req = request.values

    # 查询评论并连接用户表
    query = db.session.query(MemberComments, Member, Card). \
        join(Member, MemberComments.member_id == Member.id). \
        join(Card, MemberComments.card_id == Card.id)

    # 获取分页数据
    count = query.count()
    p = req.get('p')
    page_size = 20
    pages, offset, limit = paging(page_size, count, p)

    comment_list = query.order_by(MemberComments.id.desc()).offset(offset).limit(20).all()

    data_list = []
    if comment_list:
        # 准备数据传递给模板
        for comment, member, card in comment_list:
            data_list.append({
                "avatar": member.avatar,
                "nickname": member.nickname,
                "card_name": card.name,
                "content": comment.content,
                "score": comment.score
            })
    resp_data = {
        'list': data_list,
        'pages': pages,
        'current': 'comment'
    }
    return optRender("member/comment.html", resp_data)
