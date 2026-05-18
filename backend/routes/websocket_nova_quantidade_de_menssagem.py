from flask_socketio import emit
from models.database import Menssagens 
from routes.websocket import socketio

@socketio.on("nova_quantidade_de_menssagem")
def nova_quantidade_de_menssagem(data):
    id_destinatario = data.get("id_amigo")
    nome_destinatrio = data.get("nome_amigo")
    id_remitente = data.get("id_remitente")
    nossa_sala = data.get("nossa_sala")

    nova_quantidade_menssagem = Menssagens.query.filter_by(
        id_destinatario = id_destinatario,
        nossa_sala = nossa_sala,
        lida = False  
    ).count()
    print(f"quantidade actualizada na sala: {id_destinatario} para o meu amigo:{id_remitente}")
    emit("responsta_nova_quantidade_de_menssagem" , {"quantidade_menssagem_nao_lida":nova_quantidade_menssagem , "id_amigo":id_remitente} , room = str(id_destinatario))

