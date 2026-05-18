from flask import Blueprint, jsonify
from models.database import db, Registrar_produto, Usuario, Tabel_Reacao_Produto
from sqlalchemy import cast, Integer   # ← Adicionado

Todos_produtos = Blueprint("Todos_produtos", __name__)

@Todos_produtos.route("/buscar_todos_produtos/<int:id_usuario>", methods=["GET"])
def buscar_todos_produtos(id_usuario):
    try:
        # Fazemos um JOIN para trazer os dados do vendedor 
        # e um OUTERJOIN para as reações (porque nem todo produto tem reação)
        resultados = db.session.query(
            Registrar_produto,
            Usuario.foto_usuario,
            Tabel_Reacao_Produto.estado_adoro
        ).join(
            Usuario, Registrar_produto.id_usuario == Usuario.id
        ).outerjoin(
            Tabel_Reacao_Produto,
            (cast(Tabel_Reacao_Produto.id_produto, Integer) == Registrar_produto.id) &   # ← Lógica adicionada
            (Tabel_Reacao_Produto.id_usuario == id_usuario)
        ).all()

        lista_produto = []

        for produto, foto_vendedor, estado_adoro in resultados:

            if estado_adoro is None:
                ja_adorou = "False"
            elif estado_adoro == "0":
                ja_adorou = "False"
            else:
                ja_adorou = "True"

            item = {
                "id": produto.id,
                "nome_produto": produto.nome_produto,
                "descricao_produto": produto.descricao_produto,
                "tipo_produto": produto.tipo_produto,
                "preco_produto": produto.preco_produto,
                "url_imagem_produto": produto.url_imagem_produto,
                "id_usuario": produto.id_usuario,
                "nome_vendedor": produto.nome_vendedor,
                "foto_vendedor": foto_vendedor, # Vem direto da query otimizada
                "avalicao_produto_estrela": produto.avalicao_produto_estrela,
                "visualizacao_produto": produto.visualizacao_produto,
                "quantidade_encomenda_produto": produto.quantidade_encomenda_produto,
                "quantidade_adoro_produto": produto.quantidade_adoro_produto,
                "valor_antigo_produto": produto.valor_antigo_produto,
                "estado_adoro": ja_adorou
            }
            lista_produto.append(item)
            print(f"este é o valor do estado_adoro:{ja_adorou}")
            print(f"este é o valor o estado adoro:{estado_adoro}")
            print(type(estado_adoro))

        return jsonify(lista_produto), 200

    except Exception as erro:
        print(f"Erro ao buscar todos os produtos: {erro}")
        return jsonify({"erro": "Erro interno no servidor"}), 500