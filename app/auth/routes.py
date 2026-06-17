from flask import Blueprint
from flask import jsonify
from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from app.auth.service import AuthService
from app.core.logger import logger



auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "success": False,
            "message": "JSON inválido"
        }), 400

    email = dados.get("email")
    senha = dados.get("senha")

    usuario = AuthService.autenticar_usuario(
        email,
        senha
    )

    
    if not usuario:
        logger.warning(
    f"LOGIN_FALHA | email={email}"
)
        return jsonify({
            "success": False,
            "message": "Credenciais inválidas"
        }), 401
    
    

    login_user(usuario)
    logger.info(
    f"LOGIN_SUCESSO | usuario_id={usuario.id} | email={usuario.email}"
)

    return jsonify({
        "success": True,
        "usuario": usuario.nome
    })

@auth_bp.route(
    "/logout",
    methods=["POST"]
)



@login_required
def logout():
    
    logger.info(
    f"LOGOUT | "
    f"user_id={current_user.id}"
    )
    
    logout_user()

    return jsonify({
        "success": True,
        "message": "Logout realizado com sucesso."
    })



@auth_bp.route(
    "/me",
    methods=["GET"]
)


@login_required
def me():

    return jsonify({
        "id": current_user.id,
        "nome": current_user.nome,
        "email": current_user.email,
        "role": current_user.role
    })