from datetime import datetime, timedelta


def tempoDevolucao():
     tempo = str(datetime.now())
     manipulacao = tempo.split(' ') # 0 - y-m-d 1 - h:m:s
     temp = manipulacao[1].split('.') # 0 - h:m:s 1 - .mmm 

     tempDinamico = datetime.strptime(str(temp[0]), "%H:%M:%S")
     tempSistema = timedelta(hours=0, minutes = 2, seconds = 30) # configurar tempo final de devolução 0:02:30

     tempFinal = str(tempDinamico + tempSistema)

     tempFinal = tempFinal.split(' ')

     retorno = f'{manipulacao[0]} {tempFinal[1]}.{temp[1]}'
     return  retorno




