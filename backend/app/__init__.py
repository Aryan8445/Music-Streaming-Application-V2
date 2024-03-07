from os import path
from flask import Flask
from flask_cors import CORS

from flask_login import LoginManager
from app.config import Config
from app.extensions import db, DATABASE_NAME
from app.setup_initial_data import setup_initial_data
from app.api import api


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.app_context().push
    app.config.from_object(Config)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'

    db.init_app(app)
    api.init_app(app)
    # print("Creating Database")

    from .controllers import controllers
    from .auth import auth
    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(controllers, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.app_context().push()

    if not path.exists('instance/' + DATABASE_NAME):
        with app.app_context():
            db.create_all()
    
    setup_initial_data()
    return app


app = create_app()
