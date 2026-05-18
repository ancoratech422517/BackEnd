from models.database import Usuario , db
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from werkzeug.security import generate_password_hash

class RegisterService:
    def registrar_user_in_db(self, nome, telefone, senha , email , data_nascimento , foto_usuario , continente , pais , provincia , capital , bairro):

        # 2. Gerar o Par de Chaves Assimétricas (Para Saques/Pagamentos)
        # O RSA de 2048 bits é o padrão de segurança atual
        chave_privada_obj = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Converter Chave Privada para texto (PEM) - O usuário deve guardar isso!
        private_pem = chave_privada_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        # Converter Chave Pública para texto (PEM) - Isso vai para o BANCO
        public_pem = chave_privada_obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # 3. Criar o Hash da Senha (Criptografia Simétrica de via única)
        senha_protegida = generate_password_hash(senha)

        # 4. Salvar no SQLAlchemy
        try:
            novo_usuario = Usuario(
                nome=nome,
                telefone=telefone,
                senha_hash=senha_protegida,
                chave_publica=public_pem, # Guardamos a pública para validar saques
                foto_usuario = foto_usuario,
                email = email,
                data_nascimento = data_nascimento , 
                continente = continente,
                pais = pais,
                provincia = provincia,
                capital = capital,
                bairro = bairro
            )
            
            db.session.add(novo_usuario)
            db.session.commit()
            db.session.refresh(novo_usuario)
            db.session.remove()
            # RETORNO CRÍTICO: Você entrega a chave privada ao usuário uma única vez
            return {
                "status": "sucesso",
                "chave_privada": private_pem 
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"erro": f"Erro ao salvar no banco: {str(e)}"}, 500