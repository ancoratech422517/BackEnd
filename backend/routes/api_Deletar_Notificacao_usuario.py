from flask import Blueprint , jsonify , request
from models.database import Amizade , db
Deletar_notificacao = Blueprint("Deletar_notificacao", __name__)

@Deletar_notificacao.route("/Deletar_Notificacao_usuario" , methods = ["post"])
def Deletar_Notificacao_usuario():
    try:
        dados = request.get_json()
        id_notificacao = dados.get("id_notificacao")
        id_usuario = dados.get("id_usuario")
        tipo_notificacao = dados.get("tipo_notificacao")

        Amizade.query.filter(
            Amizade.id == id_notificacao,
            Amizade.tipo_notificacao == tipo_notificacao
        ).delete()
        db.session.commit()
        print("dados eliminado com sucesso claudio avelino")
        return jsonify({"status":"notificacao eliminada om sucesso!"})
    
    except Exception as erro:
        print(f"erro ao deletar a notificacao:{erro}")
        return jsonify({"status":f"erro ao eliminar a notificacao:{erro}"})


