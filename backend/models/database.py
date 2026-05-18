from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_usuario = db.Column(db.Text, nullable=False, default="none")
    email = db.Column(db.Text, nullable=False)
    data_nascimento = db.Column(db.Text, nullable=False)
    continente = db.Column(db.Text, nullable=False, default="none")
    pais = db.Column(db.Text, nullable=False, default="none")
    provincia = db.Column(db.Text, nullable=False, default="none")
    capital = db.Column(db.Text, nullable=False, default="none")
    bairro = db.Column(db.Text, nullable=False, default="none")

    # Criptografia assimétrica
    chave_publica = db.Column(db.Text, nullable=True) 
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.current_timestamp())

class Amizade(db.Model):
    __tablename__ = 'amizades'
    id = db.Column(db.Integer, primary_key=True)
    remetente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    status = db.Column(db.String(20), default='pendente')
    data_criacao = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    visualizada = db.Column(db.Boolean, default=False)
    foto_usuario = db.Column(db.Text, nullable=False, default="none")
    tipo_notificacao = db.Column(db.Text, nullable=False)
    imagem_produto = db.Column(db.Text, nullable=False, default="none")
    preco_produto = db.Column(db.Text, nullable=False, default="none")
    nome_produto = db.Column(db.Text, nullable=False, default="none")
    id_produto = db.Column(db.Text, nullable=False, default="none")

    remetente = db.relationship('Usuario', foreign_keys=[remetente_id])
    destinatario = db.relationship('Usuario', foreign_keys=[destinatario_id])

class Amigo(db.Model):
    __tablename__ = "meus_amigos"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_amigo = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nossa_sala = db.Column(db.String(100))
    foto_amigo = db.Column(db.Text, nullable=False, default="none")
    
    dados_amigo = db.relationship("Usuario", foreign_keys=[id_amigo])
    dados_usuario = db.relationship("Usuario", foreign_keys=[id_usuario])

class Menssagens(db.Model):
    __tablename__ = "menssagens"
    id = db.Column(db.Integer, primary_key=True)
    id_remitente = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_destinatario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nome_remitente = db.Column(db.String(100), nullable=False)
    nome_destinatario = db.Column(db.String(100), nullable=False)
    nossa_sala = db.Column(db.String(100), nullable=False, index=True)
    lida = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.String(50))
    data_envio = db.Column(db.Text, default="")
    menssagem = db.Column(db.Text, nullable=False)

    dados_remitente = db.relationship("Usuario", foreign_keys=[id_remitente])
    dados_destinatario = db.relationship("Usuario", foreign_keys=[id_destinatario])

class Registrar_produto(db.Model):
    __tablename__ = "Produto_usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    descricao_produto = db.Column(db.Text, nullable=False)
    tipo_produto = db.Column(db.Text, nullable=False)
    preco_produto = db.Column(db.Text, nullable=False)
    url_imagem_produto = db.Column(db.Text, nullable=False)
    nome_vendedor = db.Column(db.Text, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    preferencia_usuario = db.Column(db.Text, nullable=False, default="todos")
    avalicao_produto_estrela = db.Column(db.Text, nullable=False, default="0")
    visualizacao_produto = db.Column(db.Text, nullable=False, default="0")
    quantidade_encomenda_produto = db.Column(db.Text, nullable=False, default="0")
    quantidade_adoro_produto = db.Column(db.Text, nullable=False, default="0")
    valor_antigo_produto = db.Column(db.Text, nullable=False, default="none")
    comentario_produto = db.Column(db.Text, nullable=False, default="none")
    Trafego_Pago = db.Column(db.Text, nullable=False, default="False")

    dados_usuario = db.relationship("Usuario", foreign_keys=[id_usuario])

class Pedidos_Produto(db.Model):
    __tablename__ = "Pedidos_produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    nome_cliente = db.Column(db.Text, nullable=False)
    preco_produto = db.Column(db.Text, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    data_envio = db.Column(db.Text, default="")
    telefone_conta_cliente = db.Column(db.String(100), nullable=False)
    imagem_produto = db.Column(db.Text, nullable=False)
    estado_entraga = db.Column(db.Text, nullable=False, default="Pendente")
    pedido = db.Column(db.Text, nullable=False)

class Tabel_Reacao_Produto(db.Model):
    __tablename__ = "reacao_produto"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    
    # 🔥 CORRIGIDO: Deve ser Integer, não Text
    id_produto = db.Column(db.Integer, nullable=False)  
    
    estado_visualizacao = db.Column(db.Text, nullable=False, default="0")
    estado_adoro = db.Column(db.Text, nullable=False, default="0")

    dados_usuario = db.relationship("Usuario", foreign_keys=[id_usuario])
class Sistema_Trafego_Pago(db.Model):
    __tablename__ = "sistema_trafego_pago"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey("Produto_usuario.id"), nullable=False)
    nome_produto = db.Column(db.Text, nullable=False)
    preco_produto = db.Column(db.Integer, nullable=False)
    url_imagem_produto = db.Column(db.Text, nullable=False)
    valor_envestido = db.Column(db.Integer, nullable=False)
    publico_alvo = db.Column(db.Text, nullable=False)
    meta_visualizacao = db.Column(db.Integer, nullable=False)
    menus_view_ativa = db.Column(db.Text, nullable=False, default="0")
    estado_propaganda = db.Column(db.Text, nullable=False, default="ativo")
    status_trafego = db.Column(db.Text, nullable=False, default="pendente")
    pais = db.Column(db.Text, nullable=False, default="none")
    provincia = db.Column(db.Text, nullable=False, default="none")
    capital = db.Column(db.Text, nullable=False, default="none")
    bairro = db.Column(db.Text, nullable=False, default="none")
    tipo_produto = db.Column(db.Text, nullable=False)
    nome_usuario = db.Column(db.Text, nullable=False)
    telefone_usuario = db.Column(db.Text, nullable=False)
    satisfacao_cliente = db.Column(db.Text, nullable=False, default="none")
    tipo_trafego = db.Column(db.Text, nullable=False, default="none")
    data_registro_trafego = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Carteira_Digital_Depositar(db.Model):
    __tablename__ = "carteira_digital"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    numero_conta = db.Column(db.Integer, nullable=False)
    valor_sacar_conta = db.Column(db.Integer, nullable=False)