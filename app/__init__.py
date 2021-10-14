from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import secrets


# Create database:
db = SQLAlchemy()
# Name database:
DB_NAME = "db.sqlite"
# Generate random key:
GENERATED_KEY = secrets.token_urlsafe(30)
API_BASE_URL = "http://127.0.0.1:5000/"


def create_app():
    # Initialize flask:
    app = Flask(__name__)
    # Encrypt cookies and session data:
    app.config['SECRET_KEY'] = GENERATED_KEY
    # Disable track modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Database location:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialize database in this app:
    db.init_app(app)

    # Import blueprints:
    from app.controllers.agenda_controller import agenda_controller
    from app.controllers.employee_controller import employee_controller
    from app.controllers.employee_info_controller import employee_info_controller
    from app.controllers.group_controller import group_controller
    from app.controllers.kid_controller import kid_controller
    from app.controllers.kid_info_controller import kid_info_controller
    from app.controllers.shift_controller import shift_controller
    from .generator import generator

    # Register blueprints:
    app.register_blueprint(agenda_controller, url_prefix='/')
    app.register_blueprint(employee_controller, url_prefix='/')
    app.register_blueprint(employee_info_controller, url_prefix='/')
    app.register_blueprint(group_controller, url_prefix='/')
    app.register_blueprint(kid_controller, url_prefix='/')
    app.register_blueprint(kid_info_controller, url_prefix='/')
    app.register_blueprint(shift_controller, url_prefix='/')
    app.register_blueprint(generator, url_prefix='/')

    # Create database tables if needed:
    create_db_tables(app)

    return app


def create_db_tables(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
