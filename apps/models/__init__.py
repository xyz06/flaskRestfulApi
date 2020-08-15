from exts import db
from datetime import datetime

class BaseModel(db.Model):

    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

