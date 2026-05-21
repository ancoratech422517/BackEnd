from flask import Blueprint  , request , jsonify
from models.database import Tabel_Reacao_Produto, Registrar_produto , db
sistema_adoro_Ancora = Blueprint("sistema_adoro_ancora" , __name__)

@sistema_adoro_Ancora.route("/sistema_adoro_ancora" , methods = ["post"])
def SistemaAdoroAncora():
    try:
        dados = request.get_json()
        id_usuario = dados.get("id_usuario")
        id_produto = dados.get("id_produto")
        usuario = Tabel_Reacao_Produto.query.filter(
            Tabel_Reacao_Produto.id == id_usuario,
            Tabel_Reacao_Produto.id_produto == str(id_produto)
        ).first()

        if usuario:
            print("usuario existe")
            if int(usuario.estado_adoro) == 0:
                usuario.estado_adoro = 1
                
                estado_adoro_produto = Registrar_produto.query.filter(
                    Registrar_produto.id == id_produto
                ).first()
                estado_adoro_produto.quantidade_adoro_produto = int(estado_adoro_produto.quantidade_adoro_produto) + 1

                db.session.commit()

            else:
                usuario.estado_adoro = 0
                estado_adoro_produto = Registrar_produto.query.filter(
                    Registrar_produto.id == int(id_produto)
                ).first()
                estado_adoro_produto.quantidade_adoro_produto = int(estado_adoro_produto.quantidade_adoro_produto) - 1

                db.session.commit()
        else:
            print("usuario nõ existe")
            print(f"este é o id do produto:{id_produto}")
            print(f"este é o id do usuario:{id_usuario}")
            novo_dados = {
                "id_usuario":id_usuario,
                "estado_visualizacao":1,
                "estado_adoro":1,
                "id_produto":id_produto
            }
            adicionar = Tabel_Reacao_Produto(**novo_dados)
            db.session.add(adicionar)
            estado_adoro_produto = Registrar_produto.query.filter(
                    Registrar_produto.id == id_produto
                ).first()
            estado_adoro_produto.quantidade_adoro_produto = int(estado_adoro_produto.quantidade_adoro_produto) + 1
            estado_adoro_produto.visualizacao_produto = int(estado_adoro_produto.visualizacao_produto) + 1
            db.session.commit()
            
    
        print(f"este é id do produto:{id_produto}")
        return jsonify({"status":f"adoro emcrmentado com sucesso! este é o id do produto:{id_produto}"})
    except Exception as erro:
        print(f"erro ao axecutar a sistema:{erro}")
        return jsonify({"status":f"erro interno no servidor:{erro}"})
