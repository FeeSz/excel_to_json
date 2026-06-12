from app.core.database import db
from app.models.user import User


class AuthService:

    @staticmethod
    def criar_usuario(nome, email, senha, role="user"):

        usuario_existente = User.query.filter_by(
            email=email
        ).first()

        if usuario_existente:
            raise ValueError(
                "Email já cadastrado."
            )

        usuario = User(
            nome=nome,
            email=email,
            role=role
        )

        usuario.set_password(senha)

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @staticmethod
    def autenticar_usuario(email, senha):

        usuario = User.query.filter_by(
            email=email
        ).first()

        if not usuario:
            return None

        if not usuario.check_password(senha):
            return None

        if not usuario.ativo:
            return None

        return usuario