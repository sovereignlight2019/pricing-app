from flask import Flask
from config import Config

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        # Import parts of our application
        from .home import routes

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        return app