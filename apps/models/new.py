from apps.models import  BaseModel
from exts import db


class NewsType(BaseModel):
    __tablename__ = 'newstype'
    type_name = db.Column(db.String(11), unique=True, nullable=False)
    newslist = db.relationship('New',backref='newstype')



class New(BaseModel):
    __tablename__ = 'new'
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('newstype.id'), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='news')


class Comment(BaseModel):
    __tablename__ = 'comment'
    content = db.Column(db.String(255), nullable=False)
    love_num = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('new.id'))
    replys = db.relationship('Reply' , backref='comment')


class Reply(BaseModel):
    content = db.Column(db.String(255), nullable=False)
    love_num = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # to_id = db.Column(db.Integer, db.ForeignKey('user.id'))

