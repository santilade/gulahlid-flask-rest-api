from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import secrets


# Create database:
db = SQLAlchemy()
# Name database:
DB_NAME = "db.sqlite"
GENERATED_KEY = secrets.token_urlsafe(30)


def create_app():
    # Initialize flask:
    app = Flask(__name__)
    # Encrypt cookies and session data (should be randomly generated):
    app.config['SECRET_KEY'] = GENERATED_KEY

    # Database location:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Initialize database in this app:
    db.init_app(app)

    # Import controller:
    from .controller import controller
    # Register controller:
    app.register_blueprint(controller, url_prefix='/')  # Url_prefix creates subdomains

    # Create database tables if needed:
    create_db_tables(app)

    return app


def create_db_tables(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
