import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/news'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'DH39HIDNNGS9'
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(BASE_PATH,'static')
    UPLOAD_PATH = os.path.join(STATIC_PATH,'upload')
    UPLOAD_ICON_PATH = os.path.join(UPLOAD_PATH,'icon')
    UPLOAD_IMAGES_PATH = os.path.join(UPLOAD_PATH,'images')

class Development(Config):
    ENV = 'development'

class Production(Config):
    ENV = 'production'
    DEBUG = False



if __name__ == '__main__':
    print(Config.UPLOAD_ICON_PATH)