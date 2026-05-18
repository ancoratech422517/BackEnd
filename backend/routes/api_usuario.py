from flask import Blueprint, jsonify
from service.api_usuarios import UserService

users_bp = Blueprint('users', __name__)

@users_bp.route('/usuarios/lista', methods=['GET'])
def listar_usuarios():
    # Por enquanto retornamos todos
    usuarios = UserService.listar_todos_para_chat(usuario_logado_id=0) 
    return jsonify(usuarios), 200
