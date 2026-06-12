from flask_login import LoginManager
from app.models.user import User
from app.core.database import db

login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = "Faça login para acessar esta página."

login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
    User,
    int(user_id)
)