from exts import cache
from flask import request,g
from flask_restful import abort
from apps.models.user import User

def check_user():
    auth = request.headers.get('Authorization')
    if not auth:
        abort(401, msg='请先登录')
    phone = cache.get(auth)
    if not phone:
        abort(401, msg='无效令牌')
    user = User.query.filter(User.phone == phone).first()
    if not user:
        abort(401, msg='此用户已被管理员删除')
    g.user = user


def check_login(func):
    def wrapper(*args, **kwargs):
        check_user()
        return func(*args, **kwargs)
    return wrapper