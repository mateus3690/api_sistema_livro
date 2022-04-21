import repackage
repackage.up()

from src.http.api.jobAtualizarStatus import monitoraDevolucao
from database.dbase import ComponenteDB
from database.usuariosTB import usuario
from utils.manipulacaoDevolucao import tempoDevolucao
from flask_restful import Resource
from flask import request
from datetime import datetime

class LivrariaController(Resource):
     def get(self):
          param = request.args
          user = usuario(param['email'], param['senha'])  

          if user["tipo_usuario"] == "C":
               monitoraDevolucao()

          try: 
               livros = ComponenteDB(nomeTabela='tb_livros',
                                     condicoesDeConsulta =  "ind_situacao in ('A', 'F')" if user["tipo_usuario"] == "A" else "ind_situacao='A'")
               livros = livros.consultarDados()

               response = [{
                    'id':               dados[0],
                    'livro':            dados[1],
                    'autor':            dados[2],
                    'dia_cadastro':     str(dados[3]),
                    'dia_devolucao':    str(dados[4]) if dados[4] != None else "",
                    'tipo_cadastro':    "Cadastro direto" if str(dados[5]) == "A" else "Cadastro feito por usuário",
                    'status':           "ATIVO" if str(dados[6]) == "A" else "DESATIVADO",
                    'numero_publicador': dados[7],
                    'nome_publicador'  : str(dados[8])
                    } for dados in livros ]

               if response == []:
                    response = {"mensagem":"Nenhum Livro no momento"}
          
               return response

          except AttributeError:
               response = {
                    'mensagem':"Credências não existe nos registros"
               }  

          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
               if user["status"] == "Error":
                    response = user
          

          return response  
          
     
     def post(self):

          param = request.args
          user = usuario(param['email'], param['senha'])  

          try:

               dados = request.json

               data_devolucao =  'null' if user['tipo_usuario'] == "A" else f"'{str(tempoDevolucao())}'"
               livro = ComponenteDB(nomeTabela='tb_livros',
                                   inserirColunas={
                                             'livro':         f"'{dados['livro']}'",
                                             'autor':         f"'{dados['autor']}'",
                                             'dia_cadastro':  f"'{datetime.now()}'",
                                             'dia_devolucao': data_devolucao, #00:02:30 tempo padrão 
                                             'tipo_cadastro': f"'A'" if user['tipo_usuario'] == "A" else "'C'",
                                             'ind_situacao':  "'A'",
                                             'id_usuario':    user['id'] ,
                                             'publicador':    f"'{user['nome']}'"  
                                        }, salvar=True)
                                                                 
               
               livro.inserirDados()

               response = {
                    "status":"ok", 
                    "mensagem":f"Livro {dados['livro']} registrado com sucesso"
               }


          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
               if user["status"] == "Error":
                  response = user
          
          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':'Null'
               }

          except ValueError:
               response = {
                    'status':'Error',
                    'mensagem':'Erro no formato dos dados'
               }
          
          except Exception as err:
               response = {
                    'status':'500',
                    'mensagem':err
               }

          return response

     def put(self):

          param = request.args
          user = usuario(param['email'], param['senha'])  

          try:
               if user['tipo_usuario'] == "A":
                    dados = request.json
                    payload = {}

                    if 'livro' in dados:
                         payload['livro'] = f"'{dados['livro']}'"
                         
                    if 'autor' in dados:
                         payload['autor'] = f"'{dados['autor']}'"
                    
                    if 'dia_devolucao' in dados:
                         payload['dia_devolucao'] = f"'{dados['dia_devolucao']}'"
                         
                    if 'status' in dados:
                         payload['ind_situacao'] = f"'{dados['status']}'"     

                    if param['id']:
                         livro = ComponenteDB(nomeTabela='tb_livros',
                                                            valorColunaAtualizar = payload, 
                                                            condicoesDeConsulta=f"id={param['id']}",
                                                            salvar=True)
                         livro.atualizarDados()

                         response = {
                              'status':'OK',
                              'mensagem':"Dados foram atualizados com sucesso!"
                         }
                    else:
                         response = {
                                   'mensagem':"Informe ID do registro do livros!"
                              } 
               else:
                    response = {
                              'mensagem':"Somente pessoas Autorizadas"
                         }
          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }

          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
               if user["status"] == "Error":
                    response = user

          return response

     def delete(self):
          param = request.args
          user = usuario(param['email'], param['senha']) 

          try:
               if user['tipo_usuario'] == "A":

                    if param['id']:
                         livro = ComponenteDB(nomeTabela='tb_livros', 
                                                       condicoesDeConsulta=f"id={param['id']}",
                                                       salvar=True)
                         livro.apagaDados()

                         response = {
                              'status':'Ok',
                              'mensagem':'O Livro foi deletado dos registros'
                         }
                    else:
                         response = {
                                   'mensagem':"Informe ID do registro do livros!"
                              } 
                    

               else:
                    response = {
                              'mensagem':"Somente pessoas Autorizadas"
                         }

          except AttributeError:
               
               response = {
                    'status':'Error',
                    'mensagem':'Informe um registro de pronto existente'
               }
          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
               if user["status"] == "Error":
                    response = user
          
          return response
          