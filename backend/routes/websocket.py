from flask_socketio import SocketIO, emit
from flask import request
import time

# ===================== CONFIGURAÇÃO SOCKETIO =====================
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
    async_handlers=True
)

# ===================== CONTROLE ANTI-SPAM =====================
ultimo_status_enviado = {}  # {user_id: timestamp}


def get_current_user():
    """Função para obter o usuário atual a partir do token"""
    try:
        token = request.cookies.get('token_sessao')
        if not token:
            return None

        # Importações dentro da função para evitar circular imports
        from models.usuario import Usuario
        from utils.auth import decode_token  # Ajuste o caminho se necessário

        payload = decode_token(token)
        if payload and 'id' in payload:
            user = Usuario.query.get(int(payload['id']))
            return user
        return None
    except Exception as e:
        print(f"❌ Erro ao decodificar token no Socket: {e}")
        return None


# ===================== EVENTOS =====================
@socketio.on('connect')
def handle_connect():
    user = get_current_user()
    
    if not user:
        print("❌ Conexão recusada: Usuário não autenticado")
        return False  # Rejeita a conexão

    agora = time.time()
    
    # Proteção contra spam (envia status no máximo a cada 10 segundos)
    if (user.id not in ultimo_status_enviado) or (agora - ultimo_status_enviado[user.id] > 10):
        ultimo_status_enviado[user.id] = agora
        
        socketio.emit('usuario_status_alterado', {
            "usuario_id": str(user.id),
            "status": "online"
        }, broadcast=True, include_self=True)
        
        print(f"✅ Usuário {user.id} ({user.nome}) → ONLINE")
    else:
        print(f"⏭️ Status de {user.id} ignorado (enviado recentemente)")


@socketio.on('disconnect')
def handle_disconnect():
    user = get_current_user()
    if user:
        print(f"❌ Usuário {user.id} ({user.nome}) → DESCONECTADO")
        # Opcional: enviar offline após 30 segundos (pode ser implementado depois)


@socketio.on('message')
def handle_message(data):
    print(f"📨 Mensagem recebida via Socket: {data}")


# Evento opcional para quando o cliente entra em uma sala
@socketio.on('join')
def on_join(data):
    room = data.get('room')
    if room:
        join_room(room)
        print(f"Usuário entrou na sala: {room}")
