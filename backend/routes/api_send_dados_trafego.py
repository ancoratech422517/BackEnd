from flask import Blueprint , request , jsonify
from models.database import Sistema_Trafego_Pago , Registrar_produto , db , Amizade

Send_trafego_dados = Blueprint("send_trafego_dados" , __name__)

@Send_trafego_dados.route("/send_dados_trafego" , methods = ["post"])
def SendTrafegoDados ():
    try:
        dados = request.get_json()
        nome_usuario = dados.get("nome_usuario")
        telefone_usuario = dados.get("telefone_usuario")
        id_usuario = dados.get("id_usuario")
        nome_produto = dados.get("nome_produto")
        id_produto = dados.get("id_produto")
        url_imagem_produto = dados.get("imagem_produto")
        preco_produto = dados.get("preco_produto")
        valor_envestido = dados.get("valor_envestimento")
        publico_alvo = dados.get("publico_alvo")
        tipo_produto = dados.get("tipo_produto")
        pais = dados.get("pais")
        provincia = dados.get("provincia")
        capital = dados.get("capital")
        bairro = dados.get("bairro")
        print(f"este é o ID do produto:{id_produto}")

        if int(valor_envestido) == 500: 
            meta = 100      
            tipo_trafego = "basico"
        elif int(valor_envestido) == 1000:
            meta = 250
            tipo_trafego = "basico"
        elif int(valor_envestido) == 2000:
            meta = 500
            tipo_trafego = "basico"
        elif int(valor_envestido) == 5000:
            meta = 1000
            tipo_trafego = "medio"
        elif int(valor_envestido) == 10000:
            meta = 5000
            tipo_trafego = "premiun"
        produro = Registrar_produto.query.filter_by(id = id_produto).first()
        estado_visualizacao = 0
        if produro:
            estado_visualizacao = produro.visualizacao_produto
        else:
            estado_visualizacao = 0

     
        dadosTrafegoRegistrar = {
            "nome_usuario":nome_usuario,
            "telefone_usuario":telefone_usuario,
            "id_usuario":id_usuario,
            "nome_produto":nome_produto,
            "id_produto":id_produto,
            "url_imagem_produto":url_imagem_produto,
            "preco_produto":preco_produto,
            "valor_envestido":valor_envestido,
            "publico_alvo":publico_alvo,
            "tipo_produto":tipo_produto,
            "pais":pais,
            "provincia":provincia,
            "capital":capital,
            "bairro":bairro,
            "meta_visualizacao":meta,
            "menus_view_ativa":estado_visualizacao,
            "tipo_trafego":tipo_trafego
        }
        # REGISTRAR UMA NOVA NOTIFICAÇÃO NO BANCO DE DADOS DO USUARIO E DA ANCORA
        nova_notificação = {
            "destinatario_id":id_usuario,
            "remetente_id":id_usuario,
            "nome_produto":nome_produto,
            "preco_produto":preco_produto,
            "tipo_notificacao":"ancora_ecommerce",
            "imagem_produto":url_imagem_produto,
            "id_produto":id_produto,
            "status":"pendente"
        }
        novo_dados = Amizade(**nova_notificação)
        novo_trafego = Sistema_Trafego_Pago(**dadosTrafegoRegistrar)
        db.session.add(novo_trafego)
        db.session.add(novo_dados)
        db.session.commit()
        db.session.close()
        return jsonify({"status":"trafego realizado com sucesso!"})
    except Exception as erro:
        print(f"este é o erro ao tentar fazer o trafego:{erro}")
        return jsonify({"status":f"erro ao fazer o trafego:{erro}"})
    


    
    