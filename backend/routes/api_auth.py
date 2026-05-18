from flask import Blueprint, request, jsonify, make_response
from service.auth_service import AuthService
import os
import jwt
from datetime import datetime, timedelta

login_bp = Blueprint("login", __name__)

FRONTEND_URL = "https://ancora-oficial-ao.netlify.app"


# =========================
# 🔐 LOGIN
# =========================
@login_bp.route("/Login", methods=["POST"])
def Login():
    try:
        dados = request.get_json()
        telefone = dados.get("telefone")
        senha = dados.get("senha")

        resultado = AuthService.validar_login(telefone, senha)

        if not resultado:
            return jsonify({
                "menssagem": "Telefone ou senha inválidos",
                "status": "False"
            }), 401

        usuario = resultado["usuario"]
        user_id = usuario["id"]
        

        # ACCESS TOKEN
        access_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "foto_usuario":usuario["foto_usuario"],
            "email":usuario["email"],
            "pais":usuario["pais"],
            "provincia":usuario["provincia"],
            "capital":usuario["capital"],
            "bairro":usuario["bairro"],

            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }

        access_token = jwt.encode(
            access_payload,
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        # REFRESH TOKEN
        refresh_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "foto_usuario":usuario["foto_usuario"],
            "email":usuario["email"],
            "pais":usuario["pais"],
            "provincia":usuario["provincia"],
            "capital":usuario["capital"],
            "bairro":usuario["bairro"],
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        refresh_token = jwt.encode(
            refresh_payload,
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        resp = make_response(jsonify({
            "status": "True",
            "menssagem": "usuario logado!",
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "foto_usuario":usuario["foto_usuario"],
            "email":usuario["email"],
            "pais":usuario["pais"],
            "provincia":usuario["provincia"],
            "capital":usuario["capital"],
            "bairro":usuario["bairro"],

        }))

        # COOKIE ACCESS
        resp.set_cookie(
            "token_sessao",
            access_token,
            max_age=60 * 15,
            httponly=True,
            secure=True,
            samesite="None",
            path="/"
        )

        # COOKIE REFRESH
        resp.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            secure=True,
            samesite="None",
            path="/"
        )

        return resp

    except Exception as erro:
        print(f"Erro no login: {erro}")
        return jsonify({
            "status": "False",
            "menssagem": "Erro interno"
        }), 500


# =========================
# 🔄 REFRESH TOKEN (MESMO BLUEPRINT)
# =========================
@login_bp.route("/refresh", methods=["POST"])
def refresh():
    try:
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return jsonify({"erro": "Sem refresh token"}), 401

        payload = jwt.decode(
            refresh_token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )

        if payload.get("type") != "refresh":
            return jsonify({"erro": "Token inválido"}), 401

        novo_access = jwt.encode({
            "id": payload["id"],
            "nome": payload["nome"],
            "telefone": payload["telefone"],
            "foto_usuario":payload.get("foto_usuario"),
            "email":payload.get("email"),
            "pais":payload.get("pais"),
            "provincia":payload.get("provincia"),
            "capital":payload.get("capital"),
            "bairro":payload.get("bairro"),
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }, os.getenv("SECRET_KEY"), algorithm="HS256")

        resp = jsonify({"mensagem": "Token renovado"})

        resp.set_cookie(
            "token_sessao",
            novo_access,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=15 * 60,
            path="/"
        )

        return resp, 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Refresh expirado"}), 401

    except Exception as e:
        print(f"Erro refresh: {e}")
        return jsonify({"erro": "Token inválido"}), 401
