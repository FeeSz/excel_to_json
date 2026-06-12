from app import create_app

from app.auth.service import AuthService

app = create_app()

with app.app_context():

    usuario = AuthService.criar_usuario(
        nome="Administrador",
        email="admin@exceljson.com",
        senha="123456",
        role="admin"
    )

    print(usuario)