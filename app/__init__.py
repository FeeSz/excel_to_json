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
from flask import jsonify

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(upload_bp)
    @app.errorhandler(413)
    def arquivo_muito_grande(error):
        return jsonify({
            "success": False,
            "message": (
                "Arquivo excede o limite "
                "de 25 MB."
            )
        }), 413

    return app

    