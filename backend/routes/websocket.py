from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask import request
import time

socketio = SocketIO(
    logger=False, # Desliga pra não poluir. Liga só pra debug
    engineio_logger=False,
    async_mode='eventlet',
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

# Guarda sid -> user_id pra usar no disconnect
sid_por_usuario = {}
sockets_por_usuario = {} # user_id -> set de sids
ultimo_status_enviado = {}

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
        print(f"Erro ao decodificar token: {e}")
        return None

@socketio.on('connect')
def handle_connect():
    user = get_current_user()
    if not user:
        return False # Rejeita conexão sem token

    sid = request.sid
    user_id = user.id

    # 1. Guarda o mapeamento sid -> user_id pro disconnect
    sid_por_usuario[sid] = user_id

    # 2. Adiciona esse sid na lista de sockets do usuário
    if user_id not in sockets_por_usuario:
        sockets_por_usuario[user_id] = set()
    sockets_por_usuario[user_id].add(sid)

    # 3. Entra numa sala só desse usuário
    join_room(f"user_{user_id}")

    # 4. Só manda "online" se for o PRIMEIRO socket desse user
    if len(sockets_por_usuario[user_id]) == 1:
        agora = time.time()
        if (user_id not in ultimo_status_enviado) or (agora - ultimo_status_enviado[user_id] > 8):
            ultimo_status_enviado[user_id] = agora

            # IMPORTANTE: Não usa broadcast=True. Manda só pra quem precisa.
            # Ex: pra uma sala "amigos" ou "global". Por enquanto vou usar broadcast
            # mas com skip_sid pra não mandar pra socket morto
            emit('usuario_status_alterado', {
                "usuario_id": str(user_id),
                "status": "online"
            }, broadcast=True, skip_sid=sid) # não manda pra ele mesmo

            print(f"✅ Usuário {user_id} ({user.nome}) → ONLINE")
    else:
        print(f"⏭ Usuário {user_id} abriu nova aba. Total sockets: {len(sockets_por_usuario[user_id])}")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid

    # Pega o user_id pelo sid que guardamos, não pelo cookie
    user_id = sid_por_usuario.pop(sid, None)
    if not user_id:
        return

    # Remove esse sid da lista do usuário
    if user_id in sockets_por_usuario:
        sockets_por_usuario[user_id].discard(sid)

        # Se não sobrou nenhum socket, o user ficou offline
        if len(sockets_por_usuario[user_id]) == 0:
            del sockets_por_usuario[user_id]
            emit('usuario_status_alterado', {
                "usuario_id": str(user_id),
                "status": "offline"
            }, broadcast=True) # aqui pode broadcast pq ele realmente saiu
            print(f"❌ Usuário {user_id} desconectado - OFFLINE")
        else:
            print(f"⏭ Usuário {user_id} fechou uma aba. Sockets restantes: {len(sockets_por_usuario[user_id])}")

@socketio.on('join')
def on_join(data):
    room = data.get('room')
    if room:
        join_room(room)
