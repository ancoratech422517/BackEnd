from models.database import Usuario , db

class UserService:
    @staticmethod
    def listar_todos_para_chat(usuario_logado_id):
        # Buscamos todos, exceto o próprio usuário logado
        usuarios = Usuario.query.filter(Usuario.id != usuario_logado_id).all()
        
        lista_formatada = []
        for user in usuarios:
            lista_formatada.append({
                "id": user.id,
                "nome": user.nome,
                "telefone": user.telefone,
                "foto_usuario":user.foto_usuario
            })
        # db.session.commit()
        # db.session.refresh(usuarios)
        # db.session.remove()
        return lista_formatada