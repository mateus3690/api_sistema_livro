from src.config.configDB import conexao
import repackage
repackage.up()

class ComponenteDB():
    
    def __init__(self, nomeTabela = '',
                 condicoesDeConsulta = '', 
                 inserirColunas = None,
                 valorColunaAtualizar = None,
                 criarColunas = '',
                 valorConsulta = '',
                 sql='',
                 salvar = False):

        self.nomeTabela = nomeTabela
        self.criarColunas = criarColunas
        self.condicoesDeConsulta = condicoesDeConsulta
        self.inserirColunas = inserirColunas
        self.valorConsulta = valorConsulta
        self.valorColunaAtualizar = valorColunaAtualizar
        self.sql = sql
        self.salvar = salvar


    def criarTable(self):

        conn, cur = conexao()
        try:
            cur.execute(f"CREATE TABLE {self.nomeTabela} ({self.criarColunas})")       
        except:
            print('error na criação da tabela')
            return False
        if self.salvar:
            conn.commit() 
    
    def inserirDados(self):
        
        dados = self.inserirColunas
        try:
            colunas = ''
            valores = ''
            i = 0
            for chave, valor in dados.items():
                i += 1
                if i == len(dados):
                    colunas += chave
                    valores += valor
                    break
                colunas += f"{chave},"
                valores += f"{valor},"
                   
            conn, cur = conexao() 
        except AttributeError:
            print('Erro valor atribuido está incorreto!')
            return "False"
        
        sql = f'INSERT INTO {self.nomeTabela} ({colunas}) VALUES({valores})'
        #print(sql)
        try:
            cur.execute(sql)
            cur.close()
        
        except Exception as err:
            print(err)
            return False

        if self.salvar:
            conn.commit() 
    
    def consultarDados(self):
        
        sql = ''

        if self.condicoesDeConsulta != '' and self.valorConsulta != '':
            sql = f'SELECT {self.valorConsulta} FROM {self.nomeTabela} WHERE {self.condicoesDeConsulta} order by 1'
        elif self.condicoesDeConsulta != '':
            sql = f'SELECT * FROM {self.nomeTabela} WHERE {self.condicoesDeConsulta} order by 1'
        else:
           sql = f'SELECT * FROM {self.nomeTabela} order by 1' 
        #print(sql)
        conn, cur = conexao()
        try:

            cur.execute(sql)
        
        except :
            print('error ao consultar dados!')
            return False
    
        data = cur.fetchall()
        return data

    def atualizarDados(self):

        try:
            conn, cur = conexao()
            dados = self.valorColunaAtualizar
            set = ''
            i = 0
            for chave, valor in dados.items():
                i += 1
                if i == len(dados):
                    set += f'{chave} = {valor}'
                    break
                set += f'{chave} = {valor}, '
        except AttributeError:
            print('Erro valor atribuido está incorreto!')
            return False  

        sql = f"UPDATE {self.nomeTabela} SET {set} WHERE {self.condicoesDeConsulta}"
        # print(sql)
        try:
            cur.execute(sql)
        
        except Exception as err:
            # print(err)
            print('Error ao atualizar dados!')
            return False
        if self.salvar:
            conn.commit() 
    
    def apagaDados(self):

        conn, cur = conexao()
        
        sql = f'DELETE FROM {self.nomeTabela}'
        if self.condicoesDeConsulta != '':
            sql = f'DELETE FROM {self.nomeTabela} WHERE {self.condicoesDeConsulta} '

        try:
            cur.execute(sql)
        except Exception as err:
            print(err)
            print('Error ao apagar dados!')
            return False
        conn.commit()
        
    def apagarTabela(self):
    
        conn, cur = conexao()
        try:
            cur.execute(f'DROP TABLE {self.nomeTabela}')
        except Exception as err:
            print('Error ao apaga tabela')
            return False
        conn.commit()
    
    def quary(self):
        try:
            conn, cur = conexao()
            cur.execute(self.sql)
        except Exception as err:
            print(err)
            print('Error ao executar quary!')
            return False

  
