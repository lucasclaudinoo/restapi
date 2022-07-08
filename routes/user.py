from fastapi import APIRouter, Response #fastapi do fastapi
from config.db import conn #para fazer a conexão
from schemas.user import userEntity, usersEntity #importar a função 
from models.user import User #puxar a classe User
from passlib.hash import sha256_crypt #criptografar a senha
from bson import ObjectId #transforma o id em objeto
from starlette.status import HTTP_204_NO_CONTENT #codigo pra retornar no delete
#bibliotecas que usei 


user = APIRouter()


@user.get('/user') #define rota
def find_all_user():
    return usersEntity(conn.local.user.find())
    #define uma função para retornar os users do banco

@user.post('/users')
def create_user(user: User):#define a função para criar novos usuarios no banco
    new_user = dict(user)#define um novo usario usando o dicionario user
    new_user["password"] = sha256_crypt.encrypt(new_user["password"]) #define a senha do novo usuario, usando a biblioteca e criptografando
    del new_user["id"]#vai deletar o "id" que foi definidio no usuario por que o banco de dados cria um _id novo 

    id = conn.local.user.insert_one(new_user).inserted_id #daqui pra frente o id vai ser usado para inserir um novo usuario

    user = conn.local.user.find_one({"_id": id}) #user vai ser usado para retornar o id

    return userEntity(user) #vai retornar o usuario que foi criado


@user.get('/users/{id}')#define rota
def find_user(id: str):#define função para procurar usuario
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))#vai retornar um usuario usando o _id dele
                                                    #transforma o id em objeto que até então é uma str 

@user.put('/users/{id}')#define rota
def update_user(id: str, user: User): #define função para atualizar o usuario
    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)}) #vai buscar um usuario pelo id e vai atualizar com base no dicionario user
    return userEntity(conn.local.user.find_one({"_id": ObjectId})) #vai buscar o usuario pelo id e vai mostrar ele como retorno

                                                

@user.delete('/users/{id}')#define rota
def delete_user(id: str): #define a função para deletar o user
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)})) #vai buscar pelo _id e deletar o usuario que achar
    return Response(status_code=HTTP_204_NO_CONTENT) #vai retornar isso aqui