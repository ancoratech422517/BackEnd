from flask import Blueprint , request , jsonify
from models.database import db , Pedidos_Produto
from datetime import datetime
ComprarProduto = Blueprint("Comprar_produto" , __name__)

@ComprarProduto.route("/ComprarProduto" , methods = ["post"])
def Comprar_produto ():
    try:
        data = request.get_json()
        nome_cliente = data.get("nome_cliente")
        id_cliente = data.get("id_cliente")
        nome_produto = data.get("nome_produto")
        preco_produto = data.get("preco_produto")
        id_vendedor  = data.get("id_usuario_vendedor")
        telefone_conta_cliente = data.get("telefone_conta_cliente")
        urlImage = data.get("urlImage")

        dados_da_compra_do_produto_cliente = {
            "nome_cliente":nome_cliente,
            "id_cliente":id_cliente,
            "nome_produto":nome_produto,
            "preco_produto":preco_produto,
            "id_vendedor":id_vendedor,
            "telefone_conta_cliente":telefone_conta_cliente,
            "data_envio":datetime.now(),
            "imagem_produto":urlImage,
            "pedido":"meus_pedidos"
        }
        dados_da_compra_do_produto_vendedor = {
            "nome_cliente":nome_cliente,
            "id_cliente":id_cliente,
            "nome_produto":nome_produto,
            "preco_produto":preco_produto,
            "id_vendedor":id_vendedor,
            "telefone_conta_cliente":telefone_conta_cliente,
            "data_envio":datetime.now(),
            "imagem_produto":urlImage,
            "pedido":"cliente"
        }

        novo_pedido_cliente = Pedidos_Produto(**dados_da_compra_do_produto_cliente)
        db.session.add(novo_pedido_cliente)
        db.session.commit()

        novo_pedido_vendedor = Pedidos_Produto(**dados_da_compra_do_produto_vendedor)
        db.session.add(novo_pedido_vendedor)
        db.session.commit()


        return jsonify({"status":"Pagamento reealizado com sucesso!" , "dados":dados_da_compra_do_produto_vendedor})

        print(f"este é os dados da compra do produto avelino:{dados_da_compra_do_produto}")
    except Exception as erro:
        print(f"erro ao fazer o pagamento , e este é o tipo do erro:{erro}")
        return jsonify({"status":"desulpe , parece que ouve um erro ao fazer o pagamento"})
    
