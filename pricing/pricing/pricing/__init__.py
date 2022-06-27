from flask import Flask
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        # Import parts of our application
        from .home import routes

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        return app