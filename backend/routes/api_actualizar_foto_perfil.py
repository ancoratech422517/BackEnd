import re
from flask import Blueprint, jsonify, request
from models.database import Usuario, db
import cloudinary.uploader

Actualizar_foto_perfil = Blueprint("Actualizar_foto_perfil", __name__)


@Actualizar_foto_perfil.route("/actualizar_foto_perfil", methods=["POST"])
def actualizar_foto_perfil_usuario():
    try:
        foto = request.files.get("foto")
        id_usuario = request.form.get("id_usuario")

        if not foto or not id_usuario:
            return jsonify({"status": "foto e id_usuario são obrigatórios"}), 400

        # Buscar o usuário
        usuario = Usuario.query.filter_by(id=id_usuario).first()
        if not usuario:
            return jsonify({"status": "Usuário não encontrado"}), 404

        url_antiga = usuario.foto_usuario
        url_foto_actualizada = None

        # === DELETAR FOTO ANTIGA ===
        if url_antiga and "cloudinary" in url_antiga.lower():
            # Extrair public_id corretamente (sem versão)
            # Exemplo de URL: https://res.cloudinary.com/.../upload/v1234567890/usuarios/fotos_perfil/imagem.jpg
            match = re.search(r'/upload/(?:v\d+/)?(.+?)(?:\.\w+)?$', url_antiga)
            
            if match:
                public_id = match.group(1)
                print(f"Public ID para deletar: {public_id}")

                # Deletar com invalidate para limpar o CDN
                response_delete = cloudinary.uploader.destroy(
                    public_id, 
                    resource_type='image',
                    invalidate=True
                )
                print(f"Resposta da exclusão: {response_delete}")
            else:
                print("Não foi possível extrair o public_id da URL antiga.")

        # === FAZER UPLOAD DA NOVA FOTO ===
        upload_resultado = cloudinary.uploader.upload(
            foto,
            folder="usuarios/fotos_perfil",
            # overwrite=True não é necessário aqui pois estamos usando public_id único (timestamp por padrão)
            resource_type="image"
        )
        
        url_foto_actualizada = upload_resultado.get("secure_url")

        # Atualizar no banco
        usuario.foto_usuario = url_foto_actualizada
        db.session.commit()

        print(f"Imagem atualizada com sucesso: {url_foto_actualizada}")

        return jsonify({
            "status": "foto atualizada com sucesso",
            "imagem": url_foto_actualizada
        })

    except Exception as erro:
        db.session.rollback()
        print(f"Erro ao atualizar foto: {str(erro)}")
        return jsonify({"status": "Erro interno", "erro": str(erro)}), 500