from apps.models import BaseModel
from exts import db


class User(BaseModel):
    __tablename__ = 'user'

    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(120))
    phone = db.Column(db.String(11), nullable=False, unique=True)
    icon = db.Column(db.String(255), nullable=True)

    newslist = db.relationship('New', backref='author')
    comments = db.relationship('Comment', backref='user')
    replys = db.relationship('Reply', backref='user')
