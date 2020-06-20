# 应用包的构造文件

from flask import Flask

def create_app(config_name):
    app = Flask(__name__)

    # 注册API蓝图
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app