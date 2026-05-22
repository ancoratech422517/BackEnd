from flask_socketio import SocketIO, emit
from flask import request
import time

# ===================== SOCKETIO CONFIG =====================
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
    ping_interval=25
)

# ===================== CONTROLE DE STATUS =====================
ultimo_status_enviado = {}  # {user_id: timestamp}


def get_current_user():
    """Pega o usuário atual a partir do cookie/token"""
    try:
        token = request.cookies.get('token_sessao')
        if not token:
            return None
        
        # Importe aqui para evitar circular imports
        from models.usuario import Usuario
        from utils.auth import decode_token  # ajuste conforme teu projeto
        
        payload = decode_token(token)
        if payload and payload.get('id'):
            return Usuario.query.get(payload['id'])
        return None
    except:
        return None


# ===================== EVENTOS SOCKET =====================
@socketio.on('connect')
def handle_connect():
    user = get_current_user()
    
    if not user:
        print("❌ Conexão Socket recusada: Usuário não autenticado")
        return False  # rejeita a conexão

    agora = time.time()
    
    # Proteção anti-spam: só envia status a cada 10 segundos
    if (user.id not in ultimo_status_enviado) or (agora - ultimo_status_enviado[user.id] > 10):
        ultimo_status_enviado[user.id] = agora
        
        socketio.emit('usuario_status_alterado', {
            "usuario_id": str(user.id),
            "status": "online"
        }, broadcast=True, include_self=True)
        
        print(f"✅ Usuário {user.id} ({user.nome}) → ONLINE")
    else:
        print(f"⏭️ Status do usuário {user.id} ignorado (muito recente)")


@socketio.on('disconnect')
def handle_disconnect():
    user = get_current_user()
    if user:
        print(f"❌ Usuário {user.id} ({user.nome}) desconectado")
        # Opcional: enviar offline após algum tempo (pode ser melhorado depois)


@socketio.on('message')
def handle_message(data):
    print(f"Mensagem recebida: {data}")
