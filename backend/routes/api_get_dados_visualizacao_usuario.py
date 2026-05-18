from flask import Blueprint , jsonify
from models.database import Tabel_Reacao_Produto , Registrar_produto
getDadosVisualizacaoUsuario = Blueprint("getDadosVisualizacaoUsuario",__name__)

@getDadosVisualizacaoUsuario.route("/get_dados_visualizacao_usuario/<int:id_usuario>" , methods = ["get"])
def getDadosVisualizacaoUser(id_usuario):
    try:
        usuario_ativo = Tabel_Reacao_Produto.query.filter(
            Tabel_Reacao_Produto.id_usuario == id_usuario
        ).first()
        if usuario_ativo:
            return jsonify({"status":"True"})
        else:
            return jsonify({"status":"False"})
    except Exception as erro:
        return jsonify({"erro":erro})
    

