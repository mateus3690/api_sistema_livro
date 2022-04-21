from src.database.dbase import ComponenteDB
from src.database.usuariosTB import usuario
from src.utils.validadoresCampos import ValidaCampo
from flask_restful import Resource
from flask import request
from src.config.configAuth import crypMD5


class UsuarioController(Resource):
     
     def get(self):
          param = request.args
          user = usuario(param['email'], param['senha']) 

          try:
               if user['tipo_usuario'] == "A":
                    usuarios = ComponenteDB(nomeTabela='tb_usuarios')
                    usuarios = usuarios.consultarDados()

                    response = [{
                              'id':         dados[0],
                              'nome':       dados[1],
                              'email':      str(dados[2]),
                              'nascimento': str(dados[3]),
                              'data_cadastro': str(dados[4]),
                              'tipo_usuario': str(dados[5]),
                              'senha':    str(dados[6]) ,
                              'tempo_espera': str(dados[7]),
                         } for dados in usuarios]
          
                    if response == []:
                         response = {
                              "status": "Error",
                              "mensagem":"Nenhum registro de usuário no momento!"
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


     def post(self):
          
          try:
               
               dados = request.json
               analiseEmail = ValidaCampo(email=dados['email'])

               if analiseEmail.analisaEmail() == True:
                    
                    usuario = ComponenteDB(nomeTabela='tb_usuarios', 
                                           inserirColunas={
                                                       "nome":       f"'{dados['nome']}'",
                                                       "email":      f"'{dados['email']}'",
                                                       "nascimento": f"'{dados['nascimento']}'",
                                                       "tipo_usuario": f"'{dados['tipo_usuario']}'",
                                                       "senha":      f"'{crypMD5(dados['senha'] + 'TFHKKFJSTOJ8F')}'"
                                           }, salvar=True)

                    usuario.inserirDados()

                    response = {
                              "nome":       f"{dados['nome']}",
                              "email":      f"{dados['email']}",
                              "nascimento": f"{dados['nascimento']}",
                              "senha":      f"{dados['senha']}",
                    }

               elif analiseEmail.analisaEmail() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'Email inválido!'
                    }

          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
          
          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':'Null'
               }
          
          except Exception as err:
               response = {
                    'status':'500',
                    'mensagem':err
               }

          return response
               

class UsuarioControllerDetail(Resource):

     def get(self):
          param = request.args
          return usuario(param['email'], param['senha'])  
     
     def put(self):
          param = request.args
          try:
               condicao = f"email='{param['email']}' and senha='{crypMD5(param['senha'] + 'TFHKKFJSTOJ8F')}'"
               dados = request.json
               payload = {}
               
               #login para atualizar dados
               login = ComponenteDB(nomeTabela='tb_usuarios', condicoesDeConsulta=condicao)
               login = login.consultarDados()

               if login != []:

                    if 'nome' in dados:
                         payload['nome'] = f"'{dados['nome']}'"
                    
                    if 'nascimento' in dados:
                         payload['nascimento'] = f"'{dados['nascimento']}'"
                    
                    if 'senha' in dados:
                         payload['senha'] = f"'{crypMD5(dados['senha'] + 'TFHKKFJSTOJ8F')}'"

                    if 'email' in dados:
                         payload['email'] = f"'{dados['email']}'"     
                    
                    user = ComponenteDB(nomeTabela='tb_usuarios',
                                                  valorColunaAtualizar = payload, 
                                                  condicoesDeConsulta=condicao,
                                                  salvar=True)

                    user.atualizarDados()

                    response = {
                         'status':'OK',
                         'mensagem':"Dados foram atualizados com sucesso!"
                    }
               
               else:
                    response = {
                              'status':'Error',
                              'mensagem':"Verifique sua credências de login, e tente novamente!"
                    }

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }

          return response

     def delete(self):

          param = request.args
          try:
               user = ComponenteDB(nomeTabela='tb_usuarios', 
                                              condicoesDeConsulta=f"email = '{param['email']}' and senha = '{crypMD5(param['senha'] + 'TFHKKFJSTOJ8F')}'",
                                              salvar=True)
               user.apagaDados()

               response = {
                    'status':'Ok',
                    'mensagem':'O Usuário foi deletado dos registros'
               }
               
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Usuário não nos registros existente'
               }
          
          return response
