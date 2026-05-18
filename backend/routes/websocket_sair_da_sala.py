from flask_socketio import leave_room
from routes.websocket import socketio

@socketio.on("sair_da_sala")
def sair_da_sala(data):
    nossa_sala = data.get("nossa_sala")
    leave_room(nossa_sala)
    print(f"usuario saiu da sala {nossa_sala}")
    socketio.emit("usuario_saiu_da_sala" , room = str(nossa_sala))
