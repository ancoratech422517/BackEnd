from routes.websocket import socketio
from flask_socketio import emit
from models.database import Amizade, db
from datetime import datetime

@socketio.on("notificar_compra_usuario")
def notificar_compra_usuario(data):
    try:
        dados = data
        id_cliente = dados.get("id_cliente")
        id_vendedor = dados.get("id_vendedor")
        preco = dados.get("preco_produto")
        imagem = dados.get("imagem_produto")
        nome_produto = dados.get("nome_produto")

        # 1. CLIENTE recebe "você comprou"
        notificacao_usurios_compra_cliente = {
            "remetente_id": id_vendedor,  # vendedor é quem "envia" a confirmação
            "destinatario_id": id_cliente,  # cliente RECEBE
            "tipo_notificacao": "compra_produto_cliente",
            "status": "entregue",  # <- IMPORTANTE
            "data_criacao": datetime.utcnow(),  # <- IMPORTANTE
            "visualizada": False,
            "preco_produto": preco,
            "imagem_produto": imagem,
            "nome_produto":nome_produto
        }

        # 2. VENDEDOR recebe "você vendeu"
        notificacao_usurios_compra_vendedor = {
            "remetente_id": id_cliente,  # cliente é quem comprou
            "destinatario_id": id_vendedor,  # vendedor RECEBE
            "tipo_notificacao": "compra_produto_vendedor",
            "status": "entregue",
            "data_criacao": datetime.utcnow(),
            "visualizada": False,
            "preco_produto": preco,
            "imagem_produto": imagem,
            "nome_produto":nome_produto
        }

        registro_cliente_compra = Amizade(**notificacao_usurios_compra_cliente)
        registro_vendedor_compra = Amizade(**notificacao_usurios_compra_vendedor)

        db.session.add(registro_cliente_compra)
        db.session.add(registro_vendedor_compra)
        db.session.commit()

        notificacao_usurios_compra_cliente["id"] = registro_cliente_compra.id
        notificacao_usurios_compra_vendedor["id"] = registro_vendedor_compra.id

        # Emite pra sala certa
        
        emit("notificar_usuario_compra_produto", notificacao_usurios_compra_cliente, room=str(id_cliente))
        emit("notificar_usuario_compra_produto", notificacao_usurios_compra_vendedor, room=str(id_vendedor))

    except Exception as erro:
        print(f"Erro ao notificar compra: {erro}")
        emit("notificar_usuario_compra_produto", {"erro": f"erro no servidor: {erro}"})