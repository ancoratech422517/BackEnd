from flask_socketio import emit
from models.database import Menssagens , db , Registrar_produto
from routes.websocket import socketio

@socketio.on("buscar_menssagens")
def buscar_menssagens(data):
    nossa_sala = data.get("nossa_sala")

    buscar_menssagem_na_sala = Menssagens.query.filter(Menssagens.nossa_sala == nossa_sala).all()
    lista_menssagem = []
    dicionario = {}
    dadosUsers = {}
    try:  
        for menssagem in buscar_menssagem_na_sala:
            lista_menssagem.append({
            "id":menssagem.id,
            "nossa_sala": menssagem.nossa_sala,
            "menssagem": menssagem.menssagem,
            "id_remitente": menssagem.id_remitente,
            "nome_remitente": menssagem.nome_remitente,
            "id_destinatario":menssagem.id_destinatario,
            "nome_destinatario":menssagem.nome_destinatario,
            "data_envio":menssagem.data_envio,
            "lida":menssagem.lida , 
            "tipo":"texto"
            })
            dadosUsers["id_destinatario"] = menssagem.id_destinatario
            dadosUsers["id_remitente"] = menssagem.id_remitente
        #buscar os produtos do usuario
        print(f"este é o if do destinatario: {dadosUsers['id_destinatario']}")
        get_product_user_destinatario = Registrar_produto.query.filter(
             Registrar_produto.id_usuario == dadosUsers["id_destinatario"]
         )
        #buscar os produtos do remitente
        get_product_user_remitente = Registrar_produto.query.filter(
             Registrar_produto.id_usuario == dadosUsers["id_remitente"]
         )
        #aqui estamos a tratar dos produtos do destinatario
        lista_produto_usuario_destinatario = []
        for lista_produto_user in get_product_user_destinatario:
            lista_produto_usuario_destinatario.append({
                "nome_produto":lista_produto_user.nome_produto,
                "descricao_produto":lista_produto_user.descricao_produto,
                "tipo_produto":lista_produto_user.tipo_produto,
                "preco_produto":lista_produto_user.preco_produto,
                "url_imagem_produto":lista_produto_user.url_imagem_produto,
                "id_usuario":lista_produto_user.id_usuario
                
            })
        #e paramos aqui o tratamento 
        lista_produto_usuario_remitente = []
        for lista_produto_user_destinatario in get_product_user_remitente:
            lista_produto_usuario_remitente.append({
                "nome_produto":lista_produto_user_destinatario.nome_produto,
                "descricao_produto":lista_produto_user_destinatario.descricao_produto,
                "tipo_produto":lista_produto_user_destinatario.tipo_produto,
                "preco_produto":lista_produto_user_destinatario.preco_produto,
                "url_imagem_produto":lista_produto_user_destinatario.url_imagem_produto,
                "id_usuario":lista_produto_user_destinatario.id_usuario
                
            })

          

        if lista_menssagem:
            emit("minhas_menssagens" , lista_menssagem , room = str(nossa_sala))
            emit("lista_produto_usuario_chat" , lista_produto_usuario_destinatario , room = str(dadosUsers["id_remitente"]))
            emit("lista_produto_usuario_chat" , lista_produto_usuario_remitente , room = str(dadosUsers["id_destinatario"]))
            print("as menssagens foram buscadas com sucesso!")
    except Exception as erro:
        print(f"erro ao buscar as menssagens:{erro}")


  
