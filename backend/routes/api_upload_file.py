# routes/upload.py
from flask import Blueprint, request, jsonify, current_app
import uuid
import cloudinary.uploader

upload_bp = Blueprint('upload', __name__, url_prefix='/api')

# Configuração de pastas por tipo de arquivo
FOLDER_MAPPING = {
    'image': 'imagens',
    'video': 'videos',
    'raw': 'documentos',      # pdf, doc, zip, etc.
}

# Extensões permitidas (podes expandir)
ALLOWED_EXTENSIONS = {
    # Imagens
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg', 'tiff',
    # Vídeos
    'mp4', 'webm', 'mov', 'avi', 'mkv', 'flv',
    # Documentos e outros
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 
    'txt', 'csv', 'json', 'zip', 'rar'
}


def get_file_type(filename):
    """Retorna o tipo de arquivo baseado na extensão"""
    if not filename or '.' not in filename:
        return 'raw'
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg', 'tiff']:
        return 'image'
    elif ext in ['mp4', 'webm', 'mov', 'avi', 'mkv', 'flv']:
        return 'video'
    else:
        return 'raw'


@upload_bp.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "Nome do arquivo vazio"}), 400

    if not file.filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS:
        return jsonify({"success": False, "error": "Tipo de arquivo não permitido"}), 400

    try:
        # Detecta o tipo do arquivo
        file_type = get_file_type(file.filename)
        
        # Define a pasta no Cloudinary
        folder = FOLDER_MAPPING.get(file_type, 'outros')
        
        # Gera nome único
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        unique_id = str(uuid.uuid4())
        public_id = f"{folder}/{unique_id}"   # Ex: imagens/123e4567-...

        # Upload para o Cloudinary com pasta
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            resource_type="auto",           # Detecta automaticamente
            folder=folder,                  # Cria a pasta automaticamente
            overwrite=False
        )

        return jsonify({
            "success": True,
            "file_url": upload_result['secure_url'],
            "public_id": upload_result['public_id'],
            "folder": folder,
            "filename": file.filename,
            "size": upload_result['bytes'],
            "format": upload_result.get('format'),
            "resource_type": upload_result.get('resource_type')
        })

    except Exception as e:
        current_app.logger.error(f"Erro no upload Cloudinary: {str(e)}")
        return jsonify({"success": False, "error": "Erro ao fazer upload"}), 500