from models.database import Amigo , Menssagens , Usuario
from routes.websoket_conectUser import usuarios_online
class Meus_amigos:
    @staticmethod
    def Listar_todos_meus_amigos(usuario_id): 
        # Adicionei usuarios_online como argumento para facilitar
        
        meus_amigos = Amigo.query.filter(Amigo.id_usuario == usuario_id).all()

        lista_amigo = []
            
        for amigo in meus_amigos:
            # 1. Busca mensagens não lidas
            quantidade_menssagem_nao_lida = Menssagens.query.filter_by(
                 id_remitente = amigo.id_amigo,
                 nossa_sala = amigo.nossa_sala,
                 lida = False
             ).count()
            
            # 2. LÓGICA DE STATUS: Verifica se o ID do amigo está no dicionário global
            # Se o ID estiver lá, ele está 'online', senão 'offline'
            status = "online" if str(amigo.id_amigo) in usuarios_online else "offline"
            #BUSCAR A IMAGEM ACTUAL DO BANCO DE DADOS DO USUARIO
            foto_amigo_actual = Usuario.query.filter(
                Usuario.id == amigo.id_amigo
            ).first()
            amigo.foto_amigo = foto_amigo_actual.foto_usuario
            #FIM DA BUSCAR DA IMAGEM ACTUAL DO BANCO DE DADOS DO USUARIO


            lista_amigo.append({
                "id_amigo": amigo.id_amigo,
                "nossa_sala": amigo.nossa_sala,
                "nome": amigo.dados_amigo.nome,
                "foto_amigo":amigo.foto_amigo,
                "quantidade_menssagem_nao_lida": quantidade_menssagem_nao_lida,
                "status": status # <--- Envia o status atual para o Frontend
            })
            
        return lista_amigo