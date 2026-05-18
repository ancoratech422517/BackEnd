# app.py
from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask
from flask_cors import CORS
from models.database import db
from flask_talisman import Talisman
from flask_migrate import Migrate
import cloudinary

PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", "True") == "True"

from routes.websocket import socketio

# Importação dos Blueprints
from routes.api_register import registrar
from routes.api_auth import login_bp
from routes.api_usuario import users_bp
from routes.api_get_date_perfil import date_perfil_user
from routes.websocket_notificacao import notificacao
from routes.api_nitificacao_visualizada import notificacao_visualizada
from routes.api_meus_amigos import meus_amigos
from routes.api_get_quantidade_menssagem import quantidade_menssagem
from routes.api_registrar_produto import registrar_produto
from routes.api_buscar_produtos_usuario import buscar_produto_Usuario
from routes.api_upload_file import upload_bp
from routes.api_todos_produtos import Todos_produtos
from routes.api_me import login_bp as me_bp
from routes.api_logout import login_bp as logout_bp
from routes.api_ComprarProduto import ComprarProduto
from routes.api_buscar_pedidos_produtos import buscar_pedidos
from routes.api_actualizar_foto_perfil import Actualizar_foto_perfil
from routes.api_Deletar_Notificacao_usuario import Deletar_notificacao
from routes.api_visto_usuario import visto_usuario
from routes.api_sistema_adoro_ancora import sistema_adoro_Ancora
from routes.api_send_dados_trafego import Send_trafego_dados
from routes.api_Depositar_Dinheiro import Depositar_Dinheiro
from routes.api_menssage_http import messages_http_bp

import routes.websoket_conectUser
import routes.websocket_aceitar_pedido_amizade
import routes.websocket_recusar_pedido_amizade 
import routes.websocket_entrar_na_sala
import routes.websocket_enviar_menssagem
import routes.websocket_usuario_digitando
import routes.websocket_buscar_menssagens
import routes.websocket_sair_da_sala
import routes.websoket_menssagem_visualizada
import routes.websocket_nova_quantidade_de_menssagem
import routes.websocket_Eliminar_menssagem
import routes.websocket_Editar_menssagem
import routes.websocket_notificar_compra_usuario

app = Flask(__name__)

# CORS
URL_FRONTEND_ANCORA = "http://192.168.11.1:5173"
CORS(app, resources={r"/*": {
    "origins": [
        "http://127.0.0.1:5173", "http://localhost:5173", 
        "http://192.168.11.1", "http://10.140.176.115:5173"
    ],
    "supports_credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Cloudinary
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

Talisman(app, 
    content_security_policy={'default-src': "'self'", 'img-src': ["'self'", "data:", "blob:", "*.cloudinary.com"]},
    force_https=False
)

# ===================== CONFIGURAÇÃO DO NEON =====================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Ajuste caso venha com postgres://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    print("🔗 Usando Neon (PostgreSQL)")
else:
    DATABASE_URL = "sqlite:///ecommerce.db"
    print("⚠️ DATABASE_URL não encontrada → Usando SQLite local")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-desenvolvimento')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'files')
app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024

# Configurações importantes para Neon
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_timeout": 30,
    "connect_args": {
        "connect_timeout": 20,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)
socketio.init_app(app)

def setup_database():
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")

# Registro dos Blueprints
app.register_blueprint(registrar)
app.register_blueprint(users_bp)
app.register_blueprint(date_perfil_user)
app.register_blueprint(notificacao)
app.register_blueprint(notificacao_visualizada)
app.register_blueprint(meus_amigos)
app.register_blueprint(quantidade_menssagem)
app.register_blueprint(registrar_produto)
app.register_blueprint(buscar_produto_Usuario)
app.register_blueprint(upload_bp)
app.register_blueprint(Todos_produtos)
app.register_blueprint(me_bp)
app.register_blueprint(ComprarProduto)
app.register_blueprint(buscar_pedidos)
app.register_blueprint(Actualizar_foto_perfil)
app.register_blueprint(Deletar_notificacao)
app.register_blueprint(visto_usuario)
app.register_blueprint(sistema_adoro_Ancora)
app.register_blueprint(Send_trafego_dados)
app.register_blueprint(Depositar_Dinheiro)
app.register_blueprint(messages_http_bp)

if __name__ == '__main__':
    setup_database()
    
    print("=" * 70)
    print("🚀 Servidor Flask + SocketIO iniciado!")
    print(f"🌍 Porta: {PORT} | Debug: {DEBUG}")
    print(f"🔗 Banco: Neon (PostgreSQL)")
    print("=" * 70)

    socketio.run(app, host="0.0.0.0", port=PORT, debug=DEBUG, allow_unsafe_werkzeug=True)