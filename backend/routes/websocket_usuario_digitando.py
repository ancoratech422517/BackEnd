from routes.websocket import socketio 
from flask_socketio import emit

@socketio.on("digitando")
def handle_digitando(data):
    id_destinatario = data.get("id_destinatario")
    id_remitente = data.get("id_remitente")
    esta_digitando = data.get("digitando") # True ou False

    # Enviamos para a sala do destinatário
    emit("usuario_digitando", {
        "id_remitente": id_remitente,
        "digitando": esta_digitando
    }, room=str(id_destinatario))