from flask import jsonify , Blueprint
from models.database import db, Amizade , Usuario

# Rota para buscar notificações (pedidos de amizade pendentes)
notificacao = Blueprint("notificacao" , __name__)
@notificacao.route('/notificacoes/<int:usuario_id>', methods=['GET'])
def buscar_notificacoes(usuario_id):
    try:
        # Pega TODAS, não só pendente
        notificacoes = Amizade.query.filter_by(
            destinatario_id=usuario_id
        ).order_by(Amizade.data_criacao.desc()).all()
  

        # Badge só conta pedido de amizade pendente
        total_pendente = Amizade.query.filter_by(
            destinatario_id=usuario_id,
            tipo_notificacao='pedido_amizade',
            status='pendente',
            visualizada=False

        ).count()

        total_produto_vendedor = Amizade.query.filter_by(
            destinatario_id=usuario_id,
            tipo_notificacao='compra_produto_vendedor',
            visualizada=False

        ).count()

        total_produto_cliente = Amizade.query.filter_by(
            destinatario_id=usuario_id,
            tipo_notificacao='compra_produto_cliente',
            visualizada=False

        ).count()
        total_ancora_trafego = Amizade.query.filter_by(
            destinatario_id = usuario_id,
            tipo_notificacao = "ancora_ecommerce",
            visualizada=False

        ).count()

        total_quantidade_notificação = total_pendente + total_produto_cliente + total_produto_vendedor + total_ancora_trafego


        resultado = []
        for notif in notificacoes:
            print(f"este é o tipo da notificação:{notif.tipo_notificacao}")
            # BUSCAR A IMAGEM ACTUAL DO VENDEDOR
            Imagem_actual_vendedor = Usuario.query.filter(
                Usuario.id == notif.remetente_id
            ).first()
            # FIM BUSCA DA IMAGEM ACTUAL DO VENDEDOR
            remetente = Usuario.query.get(notif.remetente_id)
            if not remetente: continue  # pula se user deletado

            resultado.append({
                "id": notif.id,
                "de_id": notif.remetente_id,
                "nome_remetente": remetente.nome,
                "mensagem": f"{remetente.nome} enviou um pedido de amizade!" if notif.tipo_notificacao == 'pedido_amizade' 
                             else f"Sua Encomenda foi Confirmada data " if notif.tipo_notificacao == 'compra_produto_cliente'
                             else f"Você vendeu por {notif.preco_produto}" ,
                "data": notif.data_criacao.strftime('%d/%m/%Y %H:%M') if notif.data_criacao else "",
                "total_notificacao": total_quantidade_notificação,
                "foto_usuario": remetente.foto_usuario,
                "tipo_notificacao": notif.tipo_notificacao,
                "preco_produto": notif.preco_produto,
                "imagem_produto": notif.imagem_produto,
                "status": notif.status,
                "foto_vendedor": Imagem_actual_vendedor.foto_usuario,
                "nome_produto":notif.nome_produto
            })
            print(f"este é o tipo da notificação:{notif.tipo_notificacao}")

        return jsonify(resultado), 200

    except Exception as e:
        print(f"Erro ao buscar notificações: {e}")
        return jsonify({"erro": "Erro interno no servidor"}), 500