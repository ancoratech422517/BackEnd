from flask_socketio import join_room, leave_room, emit
from routes.websocket import socketio
from datetime import datetime 
from models.database import Menssagens , db , Amigo

@socketio.on("enviar_menssagem_na_sala")
def enviar_menssagem_na_sala(data):
    agora = datetime.now()
    horario_formatado = agora.strftime("%H:%M") 

    nossa_sala = data.get("nossa_sala")
    menssagem = data.get("menssagem")
    id_remitente = data.get("id_remitente")
    nome_remitente = data.get("nome_remitente")
    id_amigo = data.get("id_amigo")
    nome_amigo = data.get("nome_amigo")

    dados = {
        "nossa_sala": nossa_sala,
        "menssagem": menssagem,
        "id_remitente": id_remitente,
        "nome_remitente": nome_remitente,
        "id_destinatario": id_amigo,
        "nome_destinatario": nome_amigo,
        "data_envio": horario_formatado,
        "lida": False, 
        "tipo": "texto"
    }
    verificar_amizade = Amigo.query.all()


    try:
        # 1. Salva no banco de dados
        armazenar_menssagem = Menssagens(**dados)
        db.session.add(armazenar_menssagem)
        db.session.commit() # Commit aqui garante que a msg já conta no próximo passo
        print("menssagem armazenada com sucesso")
        

        # --- LÓGICA DE NOTIFICAÇÃO (BOLINHA) ---
        
        # 2. Conta quantas mensagens não lidas o DESTINATÁRIO tem NESTA sala
        quantidade = Menssagens.query.filter_by(
            id_destinatario = id_amigo,
            nossa_sala = nossa_sala,
            lida = False
        ).count()

        # 3. Envia APENAS para o destinatário a nova quantidade
        # O id_amigo no pacote é o id_remitente (quem enviou), 
        # para que o destinatário saiba de QUEM é a notificação.
        emit("responsta_nova_quantidade_de_menssagem", {
            "quantidade": quantidade,
            "id_amigo": id_remitente 
        }, room = str(id_amigo))

    except Exception as err:
        db.session.rollback()
        print(f"erro ao armazenar a menssagem: {err}")

    # 4. Envia a mensagem para a sala de chat aberta
    emit("receber_menssagem", dados, room = str(nossa_sala))