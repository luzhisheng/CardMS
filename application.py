import os
from common.libs.UrlManager import UrlManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Application(Flask):

    def __init__(self, import_name, template_folder=None, root_path=None, static_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=static_folder)
        if "ops_config" in os.environ:
            self.config.from_pyfile(f'config/{os.environ.get("ops_config")}.py')
        db.init_app(self)


db = SQLAlchemy()

app = Application(
    __name__,
    template_folder=os.getcwd() + "/web/templates/"
)

# 函数模板 模板调用flask方法
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
