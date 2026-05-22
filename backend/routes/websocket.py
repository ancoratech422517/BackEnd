from flask_socketio import SocketIO, emit, join_room
from flask import request
import time

# ===================== SOCKETIO =====================
socketio = SocketIO(
    logger=True,
    engineio_logger=True,
    async_mode='eventlet',
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.11.1:5173",
        "http://10.140.176.115:5173",
        "https://ancora-sales.netlify.app"
    ],
    ping_timeout=60,
    ping_interval=25,
    async_handlers=True
)

# ===================== CONTROLES ANTI-SPAM =====================
ultimo_status_enviado = {}      # {user_id: timestamp}
usuarios_conectados = set()     # Para evitar duplicação
ultimo_cleanup = time.time()


def get_current_user():
    try:
        token = request.cookies.get('token_sessao')
        if not token:
            return None

        from models.usuario import Usuario
        from utils.auth import decode_token

        payload = decode_token(token)
        if payload and 'id' in payload:
            return Usuario.query.get(int(payload['id']))
        return None
    except Exception as e:
        print(f"❌ Erro get_current_user: {e}")
        return None


# ===================== CONEXÃO =====================
@socketio.on('connect')
def handle_connect():
    global ultimo_cleanup
    user = get_current_user()
    
    if not user:
        print("❌ Socket recusado: Usuário não autenticado")
        return False

    agora = time.time()

    # Cleanup periódico
    if agora - ultimo_cleanup > 180:   # a cada 3 minutos
        ultimo_status_enviado.clear()
        ultimo_cleanup = agora

    # Proteção forte contra spam
    if user.id in usuarios_conectados:
        print(f"⏭️ Usuário {user.id} já está marcado como online")
        return True

    if (user.id not in ultimo_status_enviado) or (agora - ultimo_status_enviado[user.id] > 10):
        ultimo_status_enviado[user.id] = agora
        usuarios_conectados.add(user.id)

        socketio.emit('usuario_status_alterado', {
            "usuario_id": str(user.id),
            "status": "online"
        }, broadcast=True, include_self=True)

        print(f"✅ Usuário {user.id} ({user.nome}) → ONLINE")
    else:
        print(f"⏭️ Status de {user.id} ignorado (muito recente)")


@socketio.on('disconnect')
def handle_disconnect():
    user = get_current_user()
    if user:
        if user.id in usuarios_conectados:
            usuarios_conectados.discard(user.id)
        print(f"❌ Usuário {user.id} ({user.nome if user else ''}) → DESCONECTADO")


# ===================== OUTROS EVENTOS =====================
@socketio.on('join')
def on_join(data):
    room = data.get('room')
    if room:
        join_room(room)
        print(f"Usuário entrou na sala: {room}")


@socketio.on('message')
def handle_message(data):
    print(f"📨 Mensagem recebida: {data}")
