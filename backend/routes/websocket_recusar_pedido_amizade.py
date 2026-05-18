from flask_socketio import  emit , join_room
from routes.websocket import socketio
from models.database import db , Amigo , Amizade

@socketio.on("recusar_pedido_amizade")
def Recusar_pedido_amizade(data):
    id_destinatario = data.get("id_destinatario")
    id_remitente = data.get("id_remitente")
    print(f"este é o id do destinatario:{id_remitente}")
    
    #remover  usuario da tabela de notificação
    # Nota: No pedido original, o id_amigo era o destinatário e o id_usuario o remetente
    notificacao = Amizade.query.filter_by(
        remetente_id=id_remitente, 
        destinatario_id=id_destinatario
    ).first()

    if notificacao:
        db.session.delete(notificacao)
        db.session.commit()
        print("Notificação removida com sucesso!")

    else:
        print("não tem nenhuma notificaã")
        # Tenta o inverso, caso a lógica de envio tenha sido trocada
        notificacao_inversa = Amizade.query.filter_by(
            remetente_id=id_destinatario, 
            destinatario_id=id_remitente
        ).first()
        if notificacao_inversa:
            db.session.delete(notificacao_inversa)
            db.session.commit()
            print("Notificação inversa removida!")
    #fim da remoão do banco de dados do usuario

    emit("response_aceitar_pedido_amizade" , {"menssagem":"usuario regeitado"} , room = str(id_remitente))

