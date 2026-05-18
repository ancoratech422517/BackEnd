import jwt
from flask import request , jsonify
from models.database import Usuario
import os
from routes.api_auth import login_bp

@login_bp.route("/api/me", methods=["GET"])
def get_me():
    print("=== DEBUG /api/me ===")
    print("Cookies recebidos:", request.cookies)
    
    token = request.cookies.get('token_sessao')
    print("token_sessao:", token[:30] if token else None)
    
    if not token:
        print("❌ Sem token_sessao")
        return jsonify({"status": "False"}), 401
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        print("✅ Payload:", payload)
        
        usuario = Usuario.query.get(payload['id'])
        print("Usuario encontrado:", usuario)
        
        if not usuario:
            print("❌ Usuario não existe no banco")
            return jsonify({"status": "False"}), 401
            
        return jsonify({
            "status": "True",
            "id": usuario.id,
            "nome": usuario.nome,
            "telefone": usuario.telefone,
            "foto_usuario":usuario.foto_usuario,
            "email":usuario.email,
            "data_nascimento":usuario.data_nascimento,
            "continente":usuario.continente,
            "pais":usuario.pais,
            "provincia":usuario.provincia,
            "capital":usuario.capital,
            "bairro":usuario.bairro

        })
    except jwt.ExpiredSignatureError:
        print("❌ Token expirado")
        return jsonify({"status": "False", "menssagem": "Sessão expirada"}), 401
    except Exception as e:
        print(f"❌ Erro /api/me: {e}")
        return jsonify({"status": "False"}), 401