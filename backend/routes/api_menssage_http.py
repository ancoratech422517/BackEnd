# routes/messages_http.py
from flask import Blueprint, request, jsonify
import uuid
import cloudinary.uploader
from datetime import datetime
from models.database import Menssagens, db

messages_http_bp = Blueprint('messages_http', __name__, url_prefix='/api')

@messages_http_bp.route('/send-message-with-file', methods=['POST'])
def send_message_with_file():
    try:
        # Dados do formulário
        menssagem = request.form.get('menssagem', '')
        id_remitente = request.form.get('id_remitente')
        id_destinatario = request.form.get('id_destinatario')
        nossa_sala = request.form.get('nossa_sala')
        nome_remitente = request.form.get('nome_remitente')
        nome_amigo = request.form.get('nome_amigo')

        file = request.files.get('file')

        if not id_remitente or not id_destinatario or not nossa_sala:
            return jsonify({"success": False, "error": "Dados incompletos"}), 400

        file_url = None
        public_id = None
        file_name = None
        mime_type = None
        file_size = 0

        # === UPLOAD PARA CLOUDINARY ===
        if file and file.filename:
            try:
                folder = "chat_files"
                unique_id = str(uuid.uuid4())
                public_id = f"{folder}/{unique_id}"

                upload_result = cloudinary.uploader.upload(
                    file,
                    public_id=public_id,
                    folder=folder,
                    resource_type="auto"
                )

                file_url = upload_result['secure_url']
                public_id = upload_result['public_id']
                file_name = file.filename
                mime_type = file.content_type
                file_size = upload_result['bytes']

            except Exception as e:
                print(f"Erro Cloudinary: {e}")
                return jsonify({"success": False, "error": "Erro no upload do arquivo"}), 500

        # === SALVAR NO BANCO ===
        agora = datetime.now()
        horario_formatado = agora.strftime("%H:%M")

        dados = {
            "nossa_sala": nossa_sala,
            "menssagem": menssagem,
            "id_remitente": id_remitente,
            "nome_remitente": nome_remitente,
            "id_destinatario": id_destinatario,
            "nome_destinatario": nome_amigo,
            "data_envio": horario_formatado,
            "lida": False,
            "tipo": "arquivo" if file_url else "texto",
            "file_url": file_url,
            "public_id": public_id,
            "file_name": file_name,
            "mime_type": mime_type,
            "file_size": file_size
        }

        armazenar_menssagem = Menssagens(**dados)
        db.session.add(armazenar_menssagem)
        db.session.commit()

        return jsonify({
            "success": True,
            "mensagem_id": armazenar_menssagem.id,
            "file_url": file_url,
            "tipo": dados["tipo"]
        }), 201

    except Exception as err:
        db.session.rollback()
        print(f"Erro ao enviar mensagem com arquivo: {err}")
        return jsonify({"success": False, "error": "Erro interno"}), 500