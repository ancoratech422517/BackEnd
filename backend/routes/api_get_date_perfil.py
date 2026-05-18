from flask import Blueprint , request , jsonify
from models.database import Usuario, db
from service.api_get_date_perfil_service import date_perfil
date_perfil_user = Blueprint("data_perfil" , __name__)

@date_perfil_user.route("/api/getDatePerfil" , methods=["post"])
def api_get_date_pergil ():
    dados = request.get_json()
    token_user = dados.get("token")
    dados_usuario = date_perfil.dataPerfil(token_user)
    return dados_usuario

