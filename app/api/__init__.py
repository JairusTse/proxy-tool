# API蓝图的构造文件

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, errors, ips