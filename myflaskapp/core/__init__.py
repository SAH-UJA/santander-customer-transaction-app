# myflaskapp/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration settings (you can also use a separate config.py file)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['DEBUG'] = True

    # Import and register your blueprints or routes
    from ..main import main_bp
    app.register_blueprint(main_bp)

    return app
