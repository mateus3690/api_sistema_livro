from os import path
from wsgiref import headers
import repackage
repackage.up()

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config.configConexoes import AcessoENV
from src.http.controllers.usuariosController import UsuarioController, UsuarioControllerDetail
from src.http.controllers.livrariaController import LivrariaController


path = AcessoENV()
path = path.acessoAPP()
port = path['port']
path = path['versao']


app = Flask(__name__)
CORS(app)
api = Api(app)


api.add_resource(UsuarioController, f'/{path}/usuario/' )
api.add_resource(UsuarioControllerDetail, f'/{path}/usuario/restrito/' )#/<string:email>/<string:senha>

api.add_resource(LivrariaController, f'/{path}/livros/')


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=port)

     
