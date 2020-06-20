# errors.py
# 异常处理

from flask import jsonify
from . import api


# 403状态码的错误处理函数
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

