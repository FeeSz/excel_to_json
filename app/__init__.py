from flask import Flask

from app.core.config import Config
from app.core.database import db
from app.core.database import migrate
from app.core.security import login_manager
from app.auth.routes import auth_bp
from app.dashboard.routes import dashboard_bp
from app.models.user import User
from app.models.conversion_job import ConversionJob
from app.uploads.routes import upload_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(upload_bp)
    return app