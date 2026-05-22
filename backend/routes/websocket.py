from flask_socketio import SocketIO, emit
from flask import request
import time

socketio = SocketIO(
    logger=True,
    engineio_logger=True,
    async_mode='gevent',
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.11.1:5173",
        "http://10.140.176.115:5173",
        "https://ancora-sales.netlify.app"
    ],
    ping_timeout=60,
    ping_interval=25,
    # Configurações importantes para Gunicorn:
    async_handlers=True
)

ultimo_status_enviado = {}

def get_current_user():
    try:
        token = request.cookies.get('token_sessao')
        if not token:
            return None
        
        from models.usuario import Usuario
        from utils.auth import decode_token   # ajuste o caminho se necessário
        
        payload = decode_token(token)
        if payload and 'id' in payload:
            return Usuario.query.get(int(payload['id']))
        return None
    except Exception as e:
        print(f"Erro ao pegar usuário: {e}")
        return None


@socketio.on('connect')
def handle_connect():
    user = get_current_user()
    if not user:
        return False

    agora = time.time()
    
    if (user.id not in ultimo_status_enviado) or (agora - ultimo_status_enviado[user.id] > 10):
        ultimo_status_enviado[user.id] = agora
        
        socketio.emit('usuario_status_alterado', {
            "usuario_id": str(user.id),
            "status": "online"
        }, broadcast=True)

        print(f"✅ Usuário {user.id} ({user.nome}) → ONLINE")
    else:
        print(f"⏭️ Status ignorado (recente) - User {user.id}")


@socketio.on('disconnect')
def handle_disconnect():
    user = get_current_user()
    if user:
        print(f"❌ Usuário {user.id} desconectado")
