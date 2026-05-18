from models.database import Usuario, db
import jwt
import os
from flask import jsonify, current_app # Importe o current_app

class date_perfil():
    @staticmethod # Boa prática: se não usa 'self', defina como estático
    def dataPerfil(token):
        try:
            # Puxamos a chave diretamente das configurações ativas do Flask
            secret = current_app.config.get('SECRET_KEY')
            
            if not secret:
                # Log de erro para você saber o que houve no console
                print("ERRO: SECRET_KEY não configurada no Flask!")
                return jsonify({"error": "Configuração do servidor incompleta"}), 500

            # Decodificando o token
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            usuario_id = payload.get('usuario_id')

            # Limpar o cache para garantir dados frescos
            db.session.expire_all()

            # Buscar o usuario
            usuario = Usuario.query.get(usuario_id)
            
            if not usuario:
                return jsonify({"menssagem": "usuario não encontrado!"}), 404

            return jsonify({
                "status": "True",
                "nome": usuario.nome,
                "telefone": usuario.telefone,
                "id": usuario.id,
                "foto_usuario":usuario.foto_usuario
            }), 200

        except jwt.ExpiredSignatureError:
            return jsonify({"menssagem": "Token expirado!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"menssagem": "Token inválido!"}), 401
        except Exception as e:
            print(f"Erro interno: {e}")
            return jsonify({"menssagem": "Erro no servidor"}), 500