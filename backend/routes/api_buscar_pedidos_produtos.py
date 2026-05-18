from flask import Blueprint , json , jsonify
from models.database import db , Pedidos_Produto
buscar_pedidos = Blueprint("buscar_pedidos" , __name__)
@buscar_pedidos.route("/buscar_pedidos_produtos/meus_pedidos/<int:dadosUsuario_id>" , methods = ["GET"])
def BuscarPedidos(dadosUsuario_id):
    todos_pedidos = Pedidos_Produto.query.filter_by(
        id_cliente = dadosUsuario_id ,
        pedido = "meus_pedidos"
    ).all()
    print(f"este são os produtos claudio:{todos_pedidos}")
    lista_pedidos = []
    if not todos_pedidos:
        return jsonify([])
    else:
        for pedido in todos_pedidos:
            item = {
                "nome_produto":pedido.nome_produto,
                "preco_produto":pedido.preco_produto,
                "imagem_produto":pedido.imagem_produto,
                "estado_entrega":pedido.estado_entraga,
                "data_envio_produto":pedido.data_envio
            }
            lista_pedidos.append(item)
        return jsonify(lista_pedidos) , 200
    


