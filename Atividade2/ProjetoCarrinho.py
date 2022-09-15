from operator import contains
from sqlite3 import dbapi2
from fastapi import FastAPI
from typing import List
import Classes


app = FastAPI()

OK = "OK"
FALHA = "FALHA"

db_usuarios = {}
db_produtos = {}
db_end = {}        # enderecos_dos_usuarios
db_carrinhos = {}

# =======================
# === Criando usuário ===
#========================
# Salvar Usuário
def persistencia_cadastro_usuario(novo_usuario):
    db_usuarios[novo_usuario.id] = novo_usuario
    print("Registrando novo usuário: ", novo_usuario.dict())
    return OK

# Validar Usuário
# Se tiver outro usuário com o mesmo ID retornar falha
# Se o email não tiver o @ retornar falha
# Senha tem que ser maior ou igual a 3 caracteres
def regras_cadastro_usuario(novo_usuario):
    if novo_usuario.id in db_usuarios:
        return FALHA  
    if novo_usuario.email.find('@') == -1:
        return FALHA
    if len(novo_usuario.senha) < 3:
        return FALHA
    return persistencia_cadastro_usuario(novo_usuario)

# Criar um usuário      
@app.post("/usuario/")
async def criar_usuário(usuario: Classes.Usuario):
    return regras_cadastro_usuario(usuario)
    
# ===========================
# === Recuperando usuário ===
#============================
def persistencia_pesquisar_usuario(id):
    return db_usuarios[id]

# Se o id do usuário existir, retornar os dados do usuário, senão retornar falha    
def regras_pesquisar_usuario(id):
    if id in db_usuarios:
        return persistencia_pesquisar_usuario(id)
    return FALHA

@app.get("/usuario/")
async def retornar_usuario(id: int):
   return regras_pesquisar_usuario(id)

# ====================================
# === Recuperando usuário por nome ===
#=====================================

# Se existir um usuário com exatamente o mesmo nome, retornar os dados do usuário, senão retornar falha      
def regras_pesquisar_usuario_nome(nome):
    for usuario in db_usuarios.items():
        if usuario[1].nome == nome:
            return persistencia_pesquisar_usuario(usuario[1].id)

@app.get("/usuario/nome")
async def retornar_usuario_com_nome(nome: str):
    return regras_pesquisar_usuario_nome(nome)

# ====================================
# === Recuperando usuário por nome ===
#=====================================

# Se o id do usuário existir, deletar o usuário e retornar OK
# senão retornar falha
# ao deletar o usuário, deletar também endereços e carrinhos vinculados a ele
def persistencia_deletar_usuario(id):
    print(db_usuarios.pop(id))
    return OK

def regras_deletar_usuario(id):
    if id in db_usuarios:
        return persistencia_deletar_usuario(id)
    return FALHA

@app.delete("/usuario/")
async def deletar_usuario(id: int):
    return regras_deletar_usuario(id)


# Se não existir usuário com o id_usuario retornar falha, 
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar 
# uma lista vazia
### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/usuario/{id_usuario}/endereços/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    return FALHA


# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    return FALHA


# Se não existir usuário com o id_usuario retornar falha, 
# senão cria um endereço, vincula ao usuário e retornar OK
@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Classes.Endereco, id_usuario: int):
    return OK


# Se não existir endereço com o id_endereco retornar falha, 
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    return OK


# Se tiver outro produto com o mesmo ID retornar falha, 
# senão cria um produto e retornar OK
@app.post("/produto/")
async def criar_produto(produto: Classes.Produto):
    return OK


# Se não existir produto com o id_produto retornar falha, 
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    return OK


# Se não existir usuário com o id_usuario ou id_produto retornar falha, 
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK
@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    return OK


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    return Classes.CarrinhoDeCompras


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o o número de itens e o valor total do carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
    numero_itens, valor_total = 0
    return numero_itens, valor_total


# Se não existir usuário com o id_usuario retornar falha, 
# senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    return OK


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')