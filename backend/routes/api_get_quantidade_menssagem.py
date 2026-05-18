from flask import Blueprint , jsonify
from models.database import Menssagens

quantidade_menssagem = Blueprint("quantidade_menssagem" , __name__)

@quantidade_menssagem.route("/buscar_quantidade_menssagem/<int:dadosUsuario_id>/<amigo_nossa_sala>" , methods = ["GET"])
def buscar_quantidade_menssagem(dadosUsuario_id , amigo_nossa_sala):
    try:
        get_quantidade_menssagem = Menssagens.query.filter_by(
            id_destinatario = dadosUsuario_id , 
            nossa_sala = amigo_nossa_sala,
            lida = False

        ).count()

        print(f"este é a quantidade das menssagesn: {get_quantidade_menssagem}")
        return jsonify({"quantidade":get_quantidade_menssagem , "id_destinatario":dadosUsuario_id})
    except Exception as erro:
        print(f"erro ao buscar a quantidade de menssagem no banco de dados:{erro}")
       
    

    