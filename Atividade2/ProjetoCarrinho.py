import email
from operator import contains
from sqlite3 import dbapi2
from fastapi import FastAPI
from typing import List
from functools import reduce
import Classes


app = FastAPI()

OK = "OK"
FALHA = "FALHA"

ai_endereco = 0
ai_carrinho = 0

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
        print(usuario)
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
    db_usuarios.pop(id)
    return OK

def regras_deletar_usuario(id):
    if id in db_usuarios:
        return persistencia_deletar_usuario(id)
    return FALHA

@app.delete("/usuario/")
async def deletar_usuario(id: int):
    return regras_deletar_usuario(id)


# ====================================
# ========= Criando endereço =========
#=====================================

# Se não existir usuário com o id_usuario retornar falha, 
# senão cria um endereço, vincula ao usuário e retornar OK

@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Classes.Endereco, id_usuario: int):
    user = await retornar_usuario(id_usuario)
    if user != FALHA and user != None:
        print(id_usuario)
        global ai_endereco
        ai_endereco += 1
        db_end[ai_endereco] = dict({
            "id_usuario" : id_usuario,
            "endereco": endereco
        })
        print(db_end)
        return OK
    return FALHA

# Se não existir usuário com o id_usuario retornar falha, 
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar 
# uma lista vazia
### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    lista = []
    user = await retornar_usuario(id_usuario)
    if user != FALHA and user != None:
        for end in db_end.items():
            if end[1]['id_usuario'] == id_usuario:
                enderecos = {
                    "id": end[0],
                    "endereco": end[1]['endereco']
                }
                lista.append(enderecos)           
        print(lista)
        return lista
    return FALHA


# Se não existir endereço com o id_endereco retornar falha, 
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    if id_endereco in db_end:
        db_end.pop(id_endereco)
        return OK
    return FALHA

# ====================================
# ========= Retornando e-mail ========
#=====================================

# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    emails = [ email[1].email for email in db_usuarios.items() if (email[1].email).split('@')[1] == dominio]
    print(emails)
    if len(emails) > 0:
        return dict(enumerate(emails, 1))
    return FALHA

# ====================================
# ========= Produtos =================
#=====================================

# Se tiver outro produto com o mesmo ID retornar falha, 
# senão cria um produto e retornar OK
@app.post("/produto/")
async def criar_produto(produto: Classes.Produto):
    if produto.id in db_produtos:
        return FALHA
    db_produtos[produto.id] = produto
    print(db_produtos)
    return OK

@app.get("/produto/")
async def retornar_produtos():
    return  db_produtos

# Se não existir produto com o id_produto retornar falha, 
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    if id_produto in db_produtos:
        db_produtos.pop(id_produto)
        # (lembrar de desvincular o produto dos carrinhos do usuário)
        return OK
    return FALHA


# ====================================
# ========= Carrinho =================
#=====================================

def cria_carrinho(id_usuario):
    db_carrinhos[id_usuario] = {
        'id_usuario': 1,
        'id_produtos': [],
        'preco_total': 0,
        'quantidade_de_produtos': 0
    }
    
def adiciona_item_carrinho(id_usuario, id_produto, quantidade):
    db_carrinhos[id_usuario]['id_produtos'].append({
            "id": id_produto,
            "quantidade" : quantidade
        })
    #qtd_atual = db_carrinhos[id_usuario]['quantidade_de_produtos']
    db_carrinhos[id_usuario]['quantidade_de_produtos'] +=  quantidade
    
    #preco_tot_atual = db_carrinhos[id_usuario]['preco_total'] 
    db_carrinhos[id_usuario]['preco_total'] += db_produtos[id_produto].preco * quantidade
    print(db_carrinhos)
     
def atualiza_quantidade_carrinho(id_usuario):
    result = reduce(lambda x, y: x+y, db_carrinhos[id_usuario]['id_produtos'], 0)

# Se não existir usuário com o id_usuario ou id_produto retornar falha, 
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK
@app.post("/carrinho/{id_usuario}/{id_produto}/{quantidade}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int, quantidade: int):
    print(f"{id_usuario}, {id_produto}, {quantidade}")
    if not id_usuario in db_usuarios or not id_produto in db_produtos:
        return FALHA
    if not id_usuario in db_carrinhos:
        cria_carrinho(id_usuario)
        adiciona_item_carrinho(id_usuario, id_produto, quantidade)
        return OK
    else :
        adiciona_item_carrinho(id_usuario, id_produto, quantidade)
        return OK

# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
      return db_carrinhos[id_usuario]
    return FALHA

# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o o número de itens e o valor total do carrinho de compras.
@app.get("/carrinho/{id_usuario}/total")
async def retornar_total_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
        return db_carrinhos[id_usuario]['quantidade_de_produtos'], \
        db_carrinhos[id_usuario]['preco_total'] 
    return FALHA

# Se não existir usuário com o id_usuario retornar falha, 
# senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
        db_carrinhos.pop(id_usuario)
        return OK
    return FALHA


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')