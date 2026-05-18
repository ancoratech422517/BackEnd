from flask import Blueprint, jsonify
from models.database import db, Registrar_produto, Usuario

buscar_produto_Usuario = Blueprint("buscar_produto_Usuario", __name__)

@buscar_produto_Usuario.route("/buscar_produto_usuario/<int:id_usuario>", methods=["GET"])
def buscar_produto_usuario(id_usuario):
    try:
        # JOIN para trazer também a foto do vendedor
        resultados = db.session.query(
            Registrar_produto,
            Usuario.foto_usuario
        ).join(
            Usuario, Registrar_produto.id_usuario == Usuario.id
        ).filter(
            Registrar_produto.id_usuario == id_usuario
        ).all()

        array_lista = []

        for produto, foto_vendedor in resultados:
            item = {
                "id": produto.id,
                "nome_produto": produto.nome_produto,
                "descricao_produto": produto.descricao_produto,
                "tipo_produto": produto.tipo_produto,
                "preco_produto": produto.preco_produto,
                "url_imagem_produto": produto.url_imagem_produto,
                "id_usuario": produto.id_usuario,
                "nome_vendedor": produto.nome_vendedor,
                "foto_vendedor": foto_vendedor,
                "avalicao_produto_estrela": produto.avalicao_produto_estrela,
                "visualizacao_produto": produto.visualizacao_produto,
                "quantidade_encomenda_produto": produto.quantidade_encomenda_produto,
                "quantidade_adoro_produto": produto.quantidade_adoro_produto,
                "valor_antigo_produto": produto.valor_antigo_produto,
                # Como é a própria loja do usuário, não faz sentido ter "estado_adoro"
                "estado_adoro": None   # ou "False" se preferires
            }
            array_lista.append(item)

        return jsonify(array_lista), 200

    except Exception as erro:
        print(f"Erro ao buscar produtos do usuário {id_usuario}: {erro}")
        return jsonify({
            "status": "erro", 
            "detalhes": str(erro)
        }), 500