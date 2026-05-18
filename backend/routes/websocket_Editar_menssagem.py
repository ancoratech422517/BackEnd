from flask_socketio import emit
from models.database import Menssagens , db
from routes.websocket import socketio


@socketio.on("editar_menssagem")
def Editar_menssagem(data):
    id_menssagem = data.get("id_menssagem")
    sala_menssagem = data.get("sala_menssagem")
    novo_conteudo = data.get("novo_conteudo")
    id_remitente = data.get("id_remitente")
    
    editar_menssagem = Menssagens.query.filter(
        Menssagens.id == id_menssagem , 
        Menssagens.nossa_sala == sala_menssagem,
        Menssagens.id_remitente == id_remitente
    ).first()

    if editar_menssagem:
        editar_menssagem.menssagem =  novo_conteudo
        db.session.commit()
        print("menssagem actualizada com sucesso")
        socketio.emit("editar_menssagem_array" , {"id_menssagem":id_menssagem , "sala_menssagem":sala_menssagem , "novo_conteudo":novo_conteudo} , room = str(sala_menssagem) , include_self=True)
    else:
        print("falha ao editar a menssagem no bamco de dados")