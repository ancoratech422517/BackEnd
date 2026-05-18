from flask_socketio import emit, join_room
from routes.websocket import socketio
from models.database import db, Amigo, Amizade , Usuario


@socketio.on("aceitar_pedido_amizade")
def Aceitar_pedido_amizade(data):
    id_amigo = data.get("ID_destinatario")
    id_usuario = data.get("ID_remitente")
    nome_remitente = data.get("nome_remitente")
    foto_remitente = data.get("foto_remitente")
    foto_destinatario = data.get("foto_destinatario")

    print(f"avelino wy , esta é a foto do destinatario: {foto_destinatario}")


    if not id_amigo or not id_usuario:
        print("Erro: IDs inválidos recebidos")
        return

    # Ordenar para criar sala única
    ordernar_sala = sorted([int(id_usuario), int(id_amigo)])
    nossa_sala = f"sala_{ordernar_sala[0]}_{ordernar_sala[1]}"

    print(f"Processando aceitação de amizade - Sala: {nossa_sala}")
    

    # ====================== NOVA LÓGICA: VERIFICAR SE JÁ SÃO AMIGOS ======================
    # Verifica se já existe registo de amizade em qualquer sentido
    ja_sao_amigos = Amigo.query.filter(
        ((Amigo.id_usuario == id_usuario) & (Amigo.id_amigo == id_amigo)) |
        ((Amigo.id_usuario == id_amigo) & (Amigo.id_amigo == id_usuario))
    ).first()

    if ja_sao_amigos:
        print(f"Os usuários {id_usuario} e {id_amigo} já são amigos. Ignorando registo duplicado.")
    else:
        # Só regista se ainda não forem amigos
        dados_remitente = {
            "id_usuario": id_usuario,
            "id_amigo": id_amigo,
            "foto_amigo":foto_destinatario,
            "nossa_sala": nossa_sala
        }
        dados_destinatario = {
            "id_usuario": id_amigo,
            "id_amigo": id_usuario,
            "foto_amigo":foto_remitente,
            "nossa_sala": nossa_sala
        }

        novo_amigo_remitente = Amigo(**dados_remitente)
        novo_amigo_destinatario = Amigo(**dados_destinatario)

        db.session.add(novo_amigo_remitente)
        db.session.add(novo_amigo_destinatario)
        db.session.commit()
        print(f"Amizade registada com sucesso na sala: {nossa_sala}")
    # ====================================================================================

    # Remover notificação da tabela Amizade (pedido de amizade)
    notificacao = Amizade.query.filter_by(
        remetente_id=id_usuario,
        destinatario_id=id_amigo
    ).first()

    if notificacao:
        db.session.delete(notificacao)
        db.session.commit()
        print("Notificação removida com sucesso!")
    else:
        # Tenta o inverso caso a ordem esteja trocada
        notificacao_inversa = Amizade.query.filter_by(
            remetente_id=id_amigo,
            destinatario_id=id_usuario
        ).first()
        if notificacao_inversa:
            db.session.delete(notificacao_inversa)
            db.session.commit()
            print("Notificação inversa removida!")

    # Emitir respostas para ambos
    emit("response_aceitar_pedido_amizade", {
        "menssagem": f"{nome_remitente} aceitou o seu pedido de amizade",
        "nossa_sala": nossa_sala
    }, room=str(id_amigo))

    emit("response_aceitar_pedido_amizade", {
        "menssagem": "O usuário já foi notificado!",
        "nossa_sala": nossa_sala
    }, room=str(id_usuario))

    print("Processo de aceitação de amizade finalizado.")