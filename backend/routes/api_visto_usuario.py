from flask import Blueprint , request , jsonify
from models.database import Tabel_Reacao_Produto , db
from models.database import Registrar_produto
visto_usuario = Blueprint("visto_usuario" , __name__)

@visto_usuario.route("/visto_usuario" , methods = ["post"])
def VistoUsuario():
    try:
        dados_usuario = request.get_json()
        id_usuario = dados_usuario.get("id_usuario")
        id_produto = dados_usuario.get("id_produto")
        print(f"este é o id do usuario: {id_usuario}")

        get_data_table_reacao_product = Tabel_Reacao_Produto.query.filter(
            Tabel_Reacao_Produto.id_usuario == id_usuario,
            Tabel_Reacao_Produto.id_produto == id_produto
        ).first()
        
        if get_data_table_reacao_product:
            print(f"existe sim um usuario com este e esta aqui o seu valor:{get_data_table_reacao_product}")
        else:
            print(f"não existe nenhum usuario com este id: {get_data_table_reacao_product}")
            Produto = Registrar_produto.query.filter(
                Registrar_produto.id == id_produto
            ).first()
            novo_usuario = {
                "id_usuario":id_usuario,
                "estado_visualizacao":1,
                "estado_adoro":0,
                "id_produto":id_produto
            }
            adicionar = Tabel_Reacao_Produto(**novo_usuario)
            db.session.add(adicionar)
            db.session.commit()
            #------------------------------------------------------------------
            Produto.visualizacao_produto = int(Produto.visualizacao_produto) + 1 
            db.session.commit()


        return jsonify({"status":f"boas , id do usuario foi servido com sucesso:{id_produto}"})
    
    except Exception as erro:
        print(f"erro no servidor:{erro}")
        return jsonify({"status":f"erro ao pegar o id do usuario: {erro}"})
