import psycopg2
import repackage
repackage.up()

#conexão ENV
from config.configConexoes import AcessoENV
chave = AcessoENV()
chave = chave.acessoDB()

def conexao():
    try:
        conn = psycopg2.connect(database = chave['database'], 
                                user = chave['user'], 
                                password = chave['password'], 
                                host = chave['host'], 
                                port = chave['port'])
    
        cur = conn.cursor()

    except UnboundLocalError:
        print('banco indisponível!')
    except (Exception, psycopg2.DatabaseError) as error:    
        print ("Error na conexão", error)
       
    return conn, cur