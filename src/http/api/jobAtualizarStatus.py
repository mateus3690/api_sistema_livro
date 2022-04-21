from turtle import update
import repackage
from database.dbase import ComponenteDB
from datetime import datetime
repackage.up()

def monitoraDevolucao():

    condicao = f"ind_situacao='A' and tipo_cadastro = 'C'"

    livros = ComponenteDB(nomeTabela='tb_livros', condicoesDeConsulta = condicao)
    livros = livros.consultarDados()

    for dados in livros:

        devolucao = datetime.strptime(str(dados[4]), '%Y-%m-%d %H:%M:%S.%f')
        if devolucao < datetime.now():
            sql = f"""
                update tb_livros 
                set ind_situacao = 'F'
                where id = {dados[0]};

                commit;
            """
            update = ComponenteDB(sql=sql)
            update.quary()
