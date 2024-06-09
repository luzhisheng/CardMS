from web.controllers.index import route_index
from web.controllers.admin import route_admin
from web.controllers.user import route_user
from web.controllers.static import route_static
from web.controllers.account import route_account
from web.controllers.cards import route_cards
from web.controllers.member import route_member
from web.controllers.finance import route_finance
from web.controllers.stat import route_stat
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
app.register_blueprint(route_cards, url_prefix="/cards")
# /member 路径
app.register_blueprint(route_member, url_prefix="/member")
# /finance 路径
app.register_blueprint(route_finance, url_prefix="/finance")
# /stat 路径
app.register_blueprint(route_stat, url_prefix="/stat")
