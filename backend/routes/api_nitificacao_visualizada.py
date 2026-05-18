from flask import Blueprint , jsonify
from models.database import Amizade , db

notificacao_visualizada = Blueprint("notificacao_vizualizada" , __name__)

@notificacao_visualizada.route('/notificacoes/marcar_lidas/<int:usuario_id>' , methods=["get"])
def marcar_notificacoes_lidas(usuario_id):
    try:
        # 1. Filtramos apenas as notificações do destinatário que ainda não foram visualizadas
        notificacoes_pendentes = Amizade.query.filter_by(
            destinatario_id=usuario_id, 
            visualizada=False
        ).all()

        if not notificacoes_pendentes:
            return jsonify({"message": f"Nenhuma notificação nova para marcar.: {notificacoes_pendentes}"}), 200

        # 2. Loop para marcar cada uma como visualizada
        for notificacao in notificacoes_pendentes:
            notificacao.visualizada = True
            
        
        # 3. Salva as alterações no banco de dados
        db.session.commit()
        
        print(f"✅ Notificações do usuário {usuario_id} marcadas como lidas.")
        return jsonify({"status": "success", "message": "Balão zerado com sucesso!" , "dados":f"{notificacoes_pendentes}"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao atualizar notificações: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500