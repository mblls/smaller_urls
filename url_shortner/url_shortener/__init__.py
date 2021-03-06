from flask import Flask
from flask import Flask

from .extensions import db
from .routes import short



def create_app(config_file='settings.py'):
    app = Flask(__name__)

    # important to get your css loaded in, or really any of your static pages
    app.static_folder = 'templates'

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(short)

    return app

