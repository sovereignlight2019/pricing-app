import imp
from flask import Flask
from config import Config

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    with app.app_context():
        # Import parts of our application
        from .home import home
        from .register import register
        from .assetcosts import assetcosts
        from .calculator import calculator
        from .media import media

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(register.register_bp)
        app.register_blueprint(assetcosts.assetcosts_bp)
        app.register_blueprint(calculator.calculator_bp)
        app.register_blueprint(media.media_bp)
        
        return app