from flask import request
from flask_socketio import join_room, emit, disconnect
from routes.websocket import socketio
from models.database import Amizade, db, Amigo
import jwt
import os

# Dicionário global: { usuario_id: socket_sid }
usuarios_online = {}

def get_user_id_from_cookie():
    token = request.cookies.get('token_sessao')
    if not token:
        print("❌ Cookie token_sessao não encontrado")
        return None
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        
        # CRÍTICO: só aceita access token
        if payload.get("type") != "access":
            print("❌ Token não é do tipo 'access'")
            return None
            
        user_id = payload.get('id')
        print(f"✅ Token decodificado. User ID: {user_id}")
        return user_id
    except jwt.ExpiredSignatureError:
        print("❌ Access token expirado")
        return None
    except jwt.InvalidTokenError as e:
        print(f"❌ Token inválido: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao decodificar token: {e}")
        return None

@socketio.on('connect')
def handle_connect():
    print(f"\n=== SOCKET CONNECT ===")
    print(f"🔍 Nova tentativa de conexão. SID: {request.sid}")
    print(f"🔍 Origin: {request.headers.get('Origin')}")
    print(f"🔍 Cookies recebidos: {list(request.cookies.keys())}")  # Não loga o valor do token
    
    usuario_id = get_user_id_from_cookie()
    
    if not usuario_id:
        print("❌ Conexão socket rejeitada: sem token válido")
        return False  # Rejeita conexão
    
    usuario_id_str = str(usuario_id)
    usuarios_online[usuario_id_str] = request.sid
    join_room(usuario_id_str)
    
    print(f"✅ Usuário {usuario_id_str} conectado e ONLINE.")
    
    emit("usuario_status_alterado", {
        "usuario_id": usuario_id_str, 
        "status": "online"
    }, broadcast=True)
    
    return True  # Aceita explicitamente

@socketio.on('disconnect')
def handle_disconnect():
    usuario_id_desconectado = None
    
    for uid, sid in list(usuarios_online.items()):
        if sid == request.sid:
            usuario_id_desconectado = uid
            break
            
    if usuario_id_desconectado:
        del usuarios_online[usuario_id_desconectado]
        print(f"❌ Usuário {usuario_id_desconectado} desconectado e OFFLINE.")
        
        emit("usuario_status_alterado", {
            "usuario_id": usuario_id_desconectado, 
            "status": "offline"
        }, broadcast=True)

@socketio.on("enviar_pedido_de_amizade")
def enviar_pedido_de_amizade(data):
    id_remitente = get_user_id_from_cookie()
    if not id_remitente:
        emit("erro_operacao", {"msg": "Sessão expirada"}, room=request.sid)
        return disconnect()
    
    id_destinatario = data.get("id_destinatario")
    nome_remitente = data.get("nome_remitente")
    foto_usuario = data.get("foto_usuario")

    if str(id_remitente) == str(id_destinatario):
        return emit("erro_operacao", {"msg": "Não pode add a si mesmo"}, room=request.sid)

    amigo_existente = Amigo.query.filter(
        ((Amigo.id_amigo == id_destinatario) & (Amigo.id_usuario == id_remitente)) | 
        ((Amigo.id_amigo == id_remitente) & (Amigo.id_usuario == id_destinatario))
    ).first()
    
    if amigo_existente:
        return emit("erro_operacao", {"msg": "Vocês já são amigos"}, room=request.sid)

    existente = Amizade.query.filter(
        ((Amizade.remetente_id == id_remitente) & (Amizade.destinatario_id == id_destinatario)) |
        ((Amizade.remetente_id == id_destinatario) & (Amizade.destinatario_id == id_remitente))
    ).first()

    if existente:
        return emit("erro_operacao", {"msg": "Já existe uma solicitação"}, room=request.sid)

    novo_pedido = Amizade(remetente_id=id_remitente, destinatario_id=id_destinatario, status='pendente' , foto_usuario = foto_usuario , tipo_notificacao = "pedido_amizade")
    db.session.add(novo_pedido)
    db.session.commit()

    emit("receber_notificacao", {
        "tipo": "pedido_amizade",
        "mensagem": f"{nome_remitente} quer ser seu amigo",
        "id_remitente": id_remitente,
        "foto_usuario":foto_usuario
    }, room=str(id_destinatario))
    
    emit("sucesso_operacao", {"msg": "Pedido enviado"}, room=request.sid)