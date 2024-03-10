from os import path
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token


from app.config import Config
from app.extensions import db, DATABASE_NAME
from app.setup_initial_data import setup_initial_data
from app.api import api


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.app_context().push()
    app.config.from_object(Config)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'

    db.init_app(app)
    api.init_app(app)
    # print("Creating Database")
    jwt = JWTManager(app)
    from .controllers import controllers
    from .auth import auth

    app.register_blueprint(controllers, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.app_context().push()

    if not path.exists('instance/' + DATABASE_NAME):
        with app.app_context():
            db.create_all()
    
    setup_initial_data()
    return app


app = create_app()
