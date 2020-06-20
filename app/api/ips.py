from . import api
from flask import jsonify


@api.route('/ips/')
def get_ips():
    return jsonify({'id': 123, 'host': 'www.baidu.com'})