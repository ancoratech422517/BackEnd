from flask import Blueprint , jsonify
from service.api_meus_amigos_service import Meus_amigos
meus_amigos = Blueprint("meus_amigos" , __name__)

@meus_amigos.route("/api/get/meus_amigos/<int:usuario_id>" , methods = ["GET"])
def Get_meus_amigos (usuario_id):
    print(f"este é o valor da do id do remitente: {usuario_id}")
    resultado = Meus_amigos.Listar_todos_meus_amigos(usuario_id)
    
    return resultado


