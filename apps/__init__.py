from  flask import Flask
from exts import db,cache,cors
from apps.apis.newsApi import news_bp
from apps.apis.userApi import user_bp
import settings
config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Development)

    db.init_app(app=app)
    cache.init_app(app=app,config=config)
    cors.init_app(app=app, supports_credentials=True)
    app.register_blueprint(user_bp)
    app.register_blueprint(news_bp)
    print(app.url_map)
    return app