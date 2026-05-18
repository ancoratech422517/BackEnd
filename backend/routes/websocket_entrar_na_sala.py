from flask_socketio import join_room , emit , leave_room
from routes.websocket import socketio

@socketio.on("Entrar_na_sala")
def Entrar_na_sala(data):
    sala = data.get("nossa_sala")
    id_remitente = data.get("id_remitente")
    sala_antiga = data.get("sala_antiga")

    if sala_antiga:
        leave_room(sala_antiga)
        print(f"usuario saiu da sala antiga:{sala_antiga}")
    if sala and id_remitente:
        join_room(sala)
    else:
        print("o react náo enviou nenhum dados velino!")

    dados = {
        "estado":"Online"
    }
    print(f"usuario conectado na sala: {sala}")
    emit("usuario_conectado_na_sala" , room = str(sala))
