from flask import Blueprint, jsonify, current_app, session
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal,marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from apps.utils.sms import send_message
from exts import cache, db
from apps.models.user import User
from datetime import datetime
import random
import uuid

user_bp = Blueprint('user', __name__)
api = Api(user_bp)

# 自定义fields
class AuthorName(fields.Raw):
    def format(self, value):
        return value.username


news_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'datetime': fields.DateTime(attribute='create_time'),
    'author': AuthorName(attribute='author'),
    'url': fields.Url('news.newsdetail', absolute=True),
}


reply_fields = {
    'user': AuthorName(attribute='user'),
    'content': fields.String,
    'datetime': fields.DateTime(attribute='create_time'),
    'love_num': fields.Integer

}

# 评论格式
comment_fields = {
    'user': AuthorName(attribute='user'),
    'content': fields.String,
    'datetime': fields.DateTime(attribute='create_time'),
    'love_num': fields.Integer,
    'replys': fields.List(fields.Nested(reply_fields))
}





user_field = {
    'id': fields.Integer,
    'name': fields.String(attribute='username'),
    'phone': fields.String,
    'newslist' : fields.List(fields.Nested(news_fields)),
    'comments' : fields.List(fields.Nested(comment_fields))
}



class UserDetailApi(Resource):
    @marshal_with(user_field)
    def get(self, id):
        user = User.query.get(id)
        return user

api.add_resource(UserDetailApi, '/userdetail/<id>')

sms_parser = reqparse.RequestParser()
sms_parser.add_argument('phone', type=inputs.regex(r'^1[35789]\d{9}$'), help='手机格式错误', location=['form', 'args'],
                        required=True)

# 发送短信
class SendMsgApi(Resource):
    def post(self):
        args = sms_parser.parse_args()
        phone = args.get('phone')
        result, code = send_message(phone)
        current_app.logger.info(result)
        if result['statusCode'] == '000000':

            cache.set(phone, code, timeout=1000)
            return jsonify(code=200, msg='发送成功')
        else:
            current_app.logger.error(result)
            return jsonify(code=400, msg='发送失败')


lor_parser = sms_parser.copy()
lor_parser.add_argument('code', type=inputs.regex(r'^\d{4}$'), help='验证码错误', location=['form'], required=True)


# 登录或注册
class LoginOrRegister(Resource):
    def post(self):
        args = lor_parser.parse_args()
        phone = args.get('phone')
        code = args.get('code')
        print(type(code), phone)
        cache_code = cache.get(phone)
        print(cache_code, type(cache_code))

        if cache_code and code == str(cache_code):
            user = User.query.filter(User.phone == phone).first()
            if not user:
                user = User()
                user.phone = phone
                now_time = datetime.now().strftime('%Y%m%d%H%M%S')
                user.username = '用户名' + now_time
                db.session.add(user)
                db.session.commit()

            token = str(uuid.uuid4())
            print(token,'--------')
            cache.set(token, phone)
            return jsonify(code=200, msg='登录成功', token=token)

        else:
            return jsonify(code=400, msg='验证码错误')


# 图片验证码
class ForgetPasswprdApi(Resource):
    def get(self):
        words = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = ""
        for i in range(4):
            code += random.choice(words)
        session['imageCode'] = code
        return jsonify(imageCode=code)


reset_parser = sms_parser.copy()
reset_parser.add_argument('imageCode', type=inputs.regex(r'^[a-zA-W0-9]{4}$'), required=True, help='图片验证码有误')

update_parser = lor_parser.copy()
update_parser.add_argument('password', type=inputs.regex(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$'), required=True,
                           help='必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间')
update_parser.add_argument('repassword', type=inputs.regex(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$'), required=True,
                           help='必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间')

password_login_parser = sms_parser.copy()
password_login_parser.add_argument('password', type=str, required=True)


class UserApi(Resource):
    # 申请重置密码
    def get(self):
        args = reset_parser.parse_args()
        phone = args.get('phone')
        imageCode = args.get('imageCode').replace('\n', '').replace('\r', '')
        current_app.logger.info(imageCode)
        print(imageCode, '----', type(imageCode))
        code = session.get('imageCode')
        print(code, '----', type(code))
        if code and imageCode.lower() == code.lower():
            print(111)
            user = User.query.filter(User.phone == phone).first()
            if user:
                result, smscode = send_message(phone)
                current_app.logger.info(result)
                if result['statusCode'] == '000000':
                    # current_app.logger.info(result)
                    cache.set(phone, smscode, timeout=1000)
                    return jsonify(code=200, msg='发送成功')
                else:
                    current_app.logger.error(result)
                    return jsonify(code=400, msg='发送失败')
            else:
                return jsonify(code=400, msg='用户名不存在')
        else:
            return jsonify(code=400, msg='验证码有误')

    #密码登录
    def post(self):
        args = password_login_parser.parse_args()
        phone = args.get('phone')
        password = args.get('password')
        user = User.query.filter(User.phone == phone).first()
        if check_password_hash(user.password, password):
            token = str(uuid.uuid4())
            cache.set(token, phone)
            return jsonify(code=200, msg='登录成功', token=token)
        else:
            return jsonify(code=400, msg='登录失败')
    #修改密码
    def patch(self):
        args = update_parser.parse_args()
        phone = args.get('phone')
        code = args.get('code')
        pwd = args.get('password')
        reset_pwd = args.get('repassword')
        cache_code = str(cache.get(phone))

        print(code, '----', cache_code)
        print(type(code), '-----', type(cache_code))
        if cache_code and code == cache_code:
            user = User.query.filter(User.phone == phone).first()
            if pwd == reset_pwd:
                user.password = generate_password_hash(reset_pwd)
                db.session.commit()
                return jsonify(code=200, msg='密码修改成功')
            else:
                return jsonify(code=400, msg='密码不一致')
        else:
            return jsonify(code=400, msg='验证码有误')


api.add_resource(SendMsgApi, '/sms')
api.add_resource(LoginOrRegister, '/login')
api.add_resource(ForgetPasswprdApi, '/forgetPassword')
api.add_resource(UserApi, '/user')


