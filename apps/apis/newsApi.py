from flask import Blueprint, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from apps.models.new import NewsType, New, Comment
from apps.models.user import User
from apps.apis.check_user_login import check_login
from exts import db
news_bp = Blueprint('news', __name__)
api = Api(news_bp)


# 自定义fields
class AuthorName(fields.Raw):
    def format(self, value):
        return value.username


# 类别格式
type_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute='type_name')
}

# 新闻简介格式
news_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'datetime': fields.DateTime(attribute='create_time'),
    'author': AuthorName(attribute='author'),
    'url': fields.Url('news.newsdetail', absolute=True),
}
# 回复格式
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

# 新闻详情格式
news_detail_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'datetime': fields.String(attribute='create_time'),
    'author': AuthorName(attribute='author'),
    'comments': fields.List(fields.Nested(comment_fields))
}

newslist_parser = reqparse.RequestParser()
newslist_parser.add_argument('typeid', type=int, required=True)
newslist_parser.add_argument('page', type=int)


# 新闻列表
class NewsListApi(Resource):
    # 获取某个分类的新闻
    def get(self):
        args = newslist_parser.parse_args()
        typeid = args.get('typeid')
        page = args.get('page', 1)
        pagination = New.query.filter(New.type_id == typeid).paginate(page=page, per_page=8)

        data = {
            'has_more': pagination.has_next,
            'data': marshal(pagination.items, news_fields),
            'return_count': len(pagination.items),
            'html': 'null'
        }
        return data

# 新闻类型
class NewsTypeApi(Resource):
    @marshal_with(type_fields)
    def get(self):
        types = NewsType.query.all()
        return types


# 新闻详情
class NewsDetailApi(Resource):
    @marshal_with(news_detail_fields)
    def get(self, id):
        news = New.query.get(id)
        return news


news_add_parser = reqparse.RequestParser()
news_add_parser.add_argument('title', type=str, required=True, help='标题不能为空')
news_add_parser.add_argument('content', type=str, required=True, help='内容不能为空')
news_add_parser.add_argument('typeid', type=int, required=True, help='类型不能为空')

news_put_parser = news_add_parser.copy()
news_put_parser.add_argument('id', type=int, required=True, help='文章id不能为空')

news_delete_parser = reqparse.RequestParser()
news_delete_parser.add_argument('id', type=int, required=True, help='文章id不能为空')

#新闻的添加删除更新
class NewsApi(Resource):
    @check_login
    def post(self):
        args = news_add_parser.parse_args()
        title = args.get('title')
        content = args.get('content')
        typeid = args.get('typeid')
        news = New()
        news.type_id = typeid
        news.title = title
        news.content = content
        news.u_id = g.user.id

        db.session.add(news)
        db.session.commit()
        return {'code': 200, 'msg': '文章添加成功'}

    @check_login
    def put(self):
        args = news_put_parser.parse_args()
        id = args.get('id')
        title = args.get('title')
        content = args.get('content')
        typeid = args.get('typeid')
        news = New.query.filter(New.id == id).first()
        if news:
             news.title = title
             news.type_id = typeid
             news.content = content
             db.session.commit()
             return {'code': 200, 'msg': '文章修改成功'}

        else:
            return {'code': 400, 'msg': '文章修改失败'}

    @check_login
    def delete(self):
        args = news_delete_parser.parse_args()
        id = args.get('id')
        news = New.query.filter(New.id == id).first()
        if news:
            db.session.delete(news)
            db.session.commit()
            return {'code': 200, 'msg': '文章删除成功'}
        else:
            return {'code': 400, 'msg': '文章删除失败'}


api.add_resource(NewsTypeApi, '/type')
api.add_resource(NewsListApi, '/newslist')
api.add_resource(NewsDetailApi, '/newsdetail/<int:id>', endpoint='newsdetail')
api.add_resource(NewsApi, '/news')
