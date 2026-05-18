from flask_socketio import emit , join_room
from flask import json , jsonify
from models.database import Menssagens , db
from routes.websocket import socketio

@socketio.on("menssagem_visualizada")
def menssagem_visualizada (data):
    try:
        nossa_sala = data.get("nossa_sala")
        id_amigo = data.get("id_amigo") # O amigo cujas mensagens eu estou lendo
        meu_id = data.get("id_remitente") # Eu, que estou clicando
        
        # 1. Marca como lidas TODAS as mensagens que enviaram PARA MIM nesta sala
        mensagens_para_marcar = Menssagens.query.filter_by(
            nossa_sala = nossa_sala,
            id_destinatario = meu_id, # Importante: só as que EU recebi
            lida = False
        ).all()

        for msg in mensagens_para_marcar:
            msg.lida = True
        
        db.session.commit()
        print(f"Mensagens lidas por {meu_id} na sala {nossa_sala}")

        # 2. Como eu acabei de ler tudo, a MINHA quantidade de mensagens desse amigo agora é 0
        quantidade_zero = 0

        # 3. ENVIA PARA MIM MESMO (Para zerar o meu contador na tela)
        # Usamos o nome do evento que o seu Frontend já tem o ouvinte:
        emit("responsta_nova_quantidade_de_menssagem", {
            "quantidade_menssagem_nao_lida": quantidade_zero, 
            "id_amigo": id_amigo # O ID do amigo que deve ficar com 0 na minha lista
        }, room=str(meu_id))

        # 3. NOVIDADE: AVISA O AMIGO (O Remetente) que as mensagens dele foram lidas
            # Enviamos para a sala para que o Frontend dele atualize os checks
        emit("confirmacao_leitura_remetente", {
                "nossa_sala": nossa_sala,
                "lido_por": meu_id
            }, room=nossa_sala, include_self=False)

    except Exception as erro:
        db.session.rollback()
        print(f"erro ao visualizar as menssagens:{erro}")
    
    