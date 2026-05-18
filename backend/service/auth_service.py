import jwt
import datetime
import os
from werkzeug.security import check_password_hash
from models.database import Usuario, db

class AuthService:
    @staticmethod
    def validar_login(telefone, senha_pura):
        usuario = Usuario.query.filter_by(telefone=telefone).first()
        
        # Remove esses prints em produção. Vazam dados.
        # print(f"este é o primeiro dados da vverificação:{usuario}")
        # for x in usuario.query.all():
        #     print(x.nome)
        
        if not usuario or not check_password_hash(usuario.senha_hash, senha_pura):
            return None  # Falha: retorna None

        # Gera o Token mas NÃO retorna ele direto pro cliente
        token = jwt.encode({
            'usuario_id': usuario.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, os.getenv('SECRET_KEY'), algorithm="HS256")
       
        usuario_dados = {
            "id":usuario.id,
            "nome":usuario.nome,
            "telefone":usuario.telefone,
            "foto_usuario":usuario.foto_usuario,
            "email":usuario.email,
            "pais":usuario.pais,
            "provincia":usuario.provincia,
            "capital":usuario.capital,
            "bairro":usuario.bairro
        } 

        db.session.close()
        
        # Retorna dados + token separado. A rota decide o que fazer com o token
        return {
            "success": True,
            "usuario": usuario_dados,
            "token": token  # Só pra rota usar, não vai pro frontend
        }