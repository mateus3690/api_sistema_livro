from src.database.dbase import ComponenteDB
from src.config.configAuth import crypMD5

def usuario(email, senha):

    try: 
        condicao = f"email='{email}' and senha='{crypMD5(senha + 'TFHKKFJSTOJ8F')}'"

        usuario = ComponenteDB(nomeTabela='tb_usuarios', condicoesDeConsulta=condicao)
        usuario = usuario.consultarDados()
        
        response = [{
            'id':         dados[0],
            'nome':       dados[1],
            'email':      str(dados[2]),
            'nascimento': str(dados[3]),
            'data_cadastro': str(dados[4]),
            'tipo_usuario': str(dados[5]),
            'senha':    str(dados[6]) ,
            'tempo_espera': str(dados[7])  
        } for dados in usuario]

        if response == []:
            response = {
                    "status": "Error",
                    "mensagem":"Registro de usuário não encontrado!"
                    } 
        return response[0]

    except (AttributeError, TypeError):
        response = {
            'status':'Error',
            'mensagem':f"Usuário, não existe nos registros"
        } 

    except KeyError:
        response = {
            'status':'Error',
            'mensagem':f"Email ou Senha incorreto"
        } 

    return response  
 