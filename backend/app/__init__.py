from os import path
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask import request
from celery.result import AsyncResult

from app.config import Config
from app.extensions import db, DATABASE_NAME
from app.setup_initial_data import setup_initial_data




def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/1",
        result_backend="redis://localhost:6379/2",
        timezone = "Asia/kolkata",
        broker_connection_retry_on_startup=True,
    ),
    )

    db.init_app(app)
    jwt = JWTManager(app)

    from .auth import auth
    from .controllers import controllers
    from .api.playlists import api_bp as playlists_api_bp
    from .api.songs import api_bp as songs_api_bp
    from .api.albums import api_bp as albums_api_bp
    from .api.ratings import api_bp as ratings_api_bp
    from .api.search import api_bp as search_api_bp

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/api')
    app.register_blueprint(playlists_api_bp, url_prefix='/api')
    app.register_blueprint(songs_api_bp, url_prefix='/api')
    app.register_blueprint(albums_api_bp, url_prefix='/api')
    app.register_blueprint(ratings_api_bp, url_prefix='/api')
    app.register_blueprint(search_api_bp, url_prefix='/api')


    app.app_context().push()

    if not path.exists('backend/instance/' + DATABASE_NAME):
        with app.app_context():
            db.create_all()

    setup_initial_data()

    cache = Cache(app)

    return app



