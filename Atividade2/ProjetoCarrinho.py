import email
from operator import contains
from sqlite3 import dbapi2
from unittest import result
from fastapi import FastAPI
from typing import List
from functools import reduce
import Classes

app = FastAPI()

OK = "OK"
FALHA = "FALHA"

# Auto incremento para chaves
ai_endereco = 0
ai_carrinho = 0

# 'Banco' de dados
db_usuarios = {}
db_produtos = {}
db_end = {}     
db_carrinhos = {}

# ==============================================
# ============== Criando usuário ===============
#===============================================

# Salvar Usuário
def persistencia_cadastro_usuario(novo_usuario):
    db_usuarios[novo_usuario.id] = novo_usuario
    print("Registrando novo usuário: ", novo_usuario.dict())
    return OK

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
    
# ==============================================
# =========== Recuperando usuário ==============
# ==============================================

def persistencia_pesquisar_usuario(id):
    return db_usuarios[id]
 
def regras_pesquisar_usuario(id):
    if id in db_usuarios:
        return persistencia_pesquisar_usuario(id)
    return FALHA

@app.get("/usuario/")
async def retornar_usuario(id: int):
   return regras_pesquisar_usuario(id)

# ==============================================
# ====== Recuperando usuário por nome ==========
#===============================================

def regras_pesquisar_usuario_nome(nome):
    for usuario in db_usuarios.items():
        print(usuario)
        if usuario[1].nome == nome:
            return persistencia_pesquisar_usuario(usuario[1].id)

@app.get("/usuario/nome")
async def retornar_usuario_com_nome(nome: str):
    return regras_pesquisar_usuario_nome(nome)

# ==============================================
# ============= Deletando Usuário ==============
#===============================================

def persistencia_deletar_usuario(id):
    print(f'Deletando o usuário {id}.')
    db_usuarios.pop(id)
    # Deletando endereço 
    #deletar_endereco_usuario(id)
    # Deletando carrinho
    #deletar_carrinho(id)
    
    return OK

def regras_deletar_usuario(id):
    if id in db_usuarios:
        return persistencia_deletar_usuario(id)
    return FALHA

@app.delete("/usuario/")
async def deletar_usuario(id: int):
    return regras_deletar_usuario(id)

# ==============================================
# ================= Endereços ==================
#===============================================

# Criando endereço para um usuário
@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Classes.Endereco, id_usuario: int):
    user = await retornar_usuario(id_usuario)
    if user != FALHA:
        global ai_endereco
        ai_endereco += 1 
        listaEnd = {}
        
        #Recuperando a lista atual de endereço do cliente
        if id_usuario in db_end:
            listaEnd = db_end[id_usuario]["enderecos"]
        
        listaEnd[ai_endereco] = endereco
        novo_endereco = Classes.ListaDeEnderecosDoUsuario = {
            "id_usuario":id_usuario,
            "enderecos":listaEnd
            }
        db_end[id_usuario] = novo_endereco
        print(db_end)
        return OK
    return FALHA

# Retornando endereços de um usuário
@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    user = await retornar_usuario(id_usuario)
    if user != FALHA:
        for end in db_end.items():
            if end[1]['id_usuario'] == id_usuario:
                return end[1]['enderecos']       
    return FALHA

# Deletando endereço por id_endereço
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    for endereco in db_end.items():
        if id_endereco in endereco[1]['enderecos']:
            print(f'Deletando o endereço {id_endereco}')
            endereco[1]['enderecos'].pop(id_endereco)
            return OK
    return FALHA

# Deletando endereço pelo id_usuário
@app.delete("/endereco/usuario/{id_usuario}/")
async def deletar_endereco_usuario(id_usuario: int):
    if id_usuario in db_end:
        print(f'Deletando os endereços do usuário {id_usuario}.')
        db_end.pop(id_usuario)
    return OK

# ==============================================
# =================== E-mail ===================
#===============================================

#Buscando e-mails com o mesmo domínio
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    emails = [ email[1].email for email in db_usuarios.items() if (email[1].email).split('@')[1] == dominio]
    print(emails)
    if len(emails) > 0:
        return dict(enumerate(emails, 1))
    return FALHA

# ==============================================
# =================== Produtos =================
#===============================================

# Criando produto
@app.post("/produto/")
async def criar_produto(produto: Classes.Produto):
    if produto.id in db_produtos:
        return FALHA
    db_produtos[produto.id] = produto
    print(db_produtos)
    return OK

# Retornando todos os produtos
@app.get("/produto/")
async def retornar_produtos():
    return  db_produtos

# Deletando um produto pelo seu id
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    if id_produto in db_produtos:
        deletar_produto_carrinho(id_produto)
        db_produtos.pop(id_produto)
        return OK
    return FALHA

# Deletando um produto do carrinho 
def deletar_produto_carrinho(id_produto):
    for carrinho in db_carrinhos.items():
        print(carrinho)
        if id_produto in carrinho[1]["id_produtos"]:
            print(f"Deletando o produto {id_produto}")
            
            #Descontando o valor e quantidade do item retirado
            qtdProdRemov        = carrinho[1]["id_produtos"][id_produto]["quantidade"]
            precoTotProdRemov   = db_produtos[id_produto].preco * qtdProdRemov     
            db_carrinhos[1]['quantidade_de_produtos'] -=  qtdProdRemov
            db_carrinhos[1]['preco_total'] -=  precoTotProdRemov
            
            carrinho[1]["id_produtos"].pop(id_produto)
            
# ==============================================
# ================== Carrinho ==================
#===============================================

# Criando carrinho vazio
def cria_carrinho(id_usuario):
    db_carrinhos[id_usuario] = {
        'id_usuario': 1,
        'id_produtos': {},
        'preco_total': 0,
        'quantidade_de_produtos': 0
    }
 
# Adicionando item no carrinho e somando os totais de produtos e preço   
def adiciona_item_carrinho(id_usuario, id_produto, quantidade):
    db_carrinhos[id_usuario]['id_produtos'][id_produto]=({
            "id": id_produto,
            "quantidade" : quantidade
        })
    db_carrinhos[id_usuario]['quantidade_de_produtos'] +=  quantidade
    db_carrinhos[id_usuario]['preco_total'] += db_produtos[id_produto].preco * quantidade
    print(db_carrinhos)
 
# Adicionando item no carrinho   
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

# Buscando carrinho de um usuário
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
      return db_carrinhos[id_usuario]
    return FALHA

# Buscando total do carrinho de um usuário
@app.get("/carrinho/{id_usuario}/total")
async def retornar_total_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
        return db_carrinhos[id_usuario]['quantidade_de_produtos'], \
        db_carrinhos[id_usuario]['preco_total'] 
    return FALHA

# Deletando o carrinho de um usuário
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
        db_carrinhos.pop(id_usuario)
        print(f"Deletando o carrinho do usuario {id_usuario} ")
        return OK
    return FALHA


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')