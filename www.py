from web.controllers.index import route_index
from web.controllers.admin import route_admin
from web.controllers.user import route_user
from web.controllers.static import route_static
from web.controllers.account import route_account
from web.controllers.card import route_card
from web.controllers.member import route_member
from web.controllers.finance import route_finance
from web.controllers.stat import route_stat
from web.controllers.upload import route_upload
from web.controllers.chart import route_chart
from web.controllers.sys import route_sys
from application import app
# 拦截器
from web.controllers.auth_interceptor import *

# 首页路径
app.register_blueprint(route_index, url_prefix="/")
# 后台路径
app.register_blueprint(route_admin, url_prefix="/admin")
# /user 路径
app.register_blueprint(route_user, url_prefix="/user")
# /static 路径
app.register_blueprint(route_static, url_prefix="/static")
# /account 路径
app.register_blueprint(route_account, url_prefix="/account")
# /food 路径
app.register_blueprint(route_card, url_prefix="/card")
# /member 路径
app.register_blueprint(route_member, url_prefix="/member")
# /finance 路径
app.register_blueprint(route_finance, url_prefix="/finance")
# /stat 路径
app.register_blueprint(route_stat, url_prefix="/stat")
# /route_upload 路径
app.register_blueprint(route_upload, url_prefix="/upload")
# /route_upload 路径
app.register_blueprint(route_chart, url_prefix="/chart")
# /sys 路径
app.register_blueprint(route_sys, url_prefix="/sys")
