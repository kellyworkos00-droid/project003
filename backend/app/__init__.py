from flask import Flask
from flask_cors import CORS
import os


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    CORS(app)

    # Late imports to avoid circular refs
    from app.routes.contacts import contacts_bp
    from app.routes.deals import deals_bp
    from app.auth import auth_bp

    app.register_blueprint(contacts_bp, url_prefix="/contacts")
    app.register_blueprint(deals_bp, url_prefix="/deals")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
