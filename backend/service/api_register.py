from models.api_register_db import RegisterService
from flask import json , jsonify
models = RegisterService()

class register_user():
    def __init__(self):
        self.registrar_usuario()
    def registrar_usuario(self , 
                          nome=None , 
                          telefone=None , 
                          senha=None , 
                          confirmar_senha=None , 
                          email = None , 
                          data_nascimento = None , 
                          foto = None,
                          continente = None,
                          pais = None , 
                          provincia = None,
                          capital = None,
                          bairro = None
                          ):
        if not senha:
            return "senha invalida"
        elif len(senha) < 6:
            return "tens que digita acime de 5 caracteres"
        elif senha != confirmar_senha:
            return "as senhas não coicidem"
        elif not nome:
            return "campo do nome obrigatorio"
        elif not telefone:
            return "campo do telefone obrigatorio"
        else:
            dados = {
                "nome":nome,
                "telefone":telefone,
                "senha":senha,
                # "confirmar_senha":confirmar_senha,
                "email":email,
                "data_nascimento":data_nascimento,
                "foto_usuario":foto,
                "continente":continente,
                "pais":pais,
                "provincia":provincia,
                "capital":capital,
                "bairro":bairro
            }
            models.registrar_user_in_db(**dados)
            return "usuario registrado com sucesso"