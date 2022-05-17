import time
import bot_web_scraping
import bot_registro_excel
import bot_envio_email


print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("----- Ola! Para obter os dados sobre a vulnerabilidade siga os passos a seguir. -----")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
ListaEmails = [
    'gelsinhomusico@gmail.com'
]
#'gelsinhomusico@gmail.com',
#    '2.gelsinhomusico@gmail.com',  

while True: # While do EMAIL
    email_desejado = input("Digite o email para onde enviaremos os resultados: ")
    if ('@' not in email_desejado) or ('.' not in email_desejado):
        print('Email invalido, por gentileza digite novamente.')
        continue
    else:
        ListaEmails.append(email_desejado)
    resp = input("Deseja inserir outro email?[Y/N]")
    print(resp)
    while True:        
        if resp.lower() == 'y' or resp.lower() == 'n':
            break
        else:
            resp = input("Deseja inserir outro email?[Y/N]")
            continue
    if resp.lower() == 'y':
        continue
    else:
        break


while True: # While do Software
    sw_sch = input("Insira o software que deseja pesquisar: ")#"log4J"
    if sw_sch == '':
        print('Dado invalido, digite novamente')
        continue
    else:
        break    

while True: #* Testador de datas SIMPLIFICADO, é necessario que as datas
    while True:
        data_busca = input("Insira a data de início do intervalo (formato mmddYY): ")#"01152022" #! A entrada de data deve estar no padrão americano mm dd YY
        data_busca = data_busca.replace("/", "")
        data_busca = data_busca.replace(" ", "")
        if int(data_busca[0:2]) > 12:
            print("Mes invalido")
            continue
        elif int(data_busca[2:4]) >= 32:
            print("Dia invalido")
            continue
        elif (int(data_busca[0:2]) == 2) and (int(data_busca[2:4]) > 30):
            print("Dia invalido")
            continue
        elif len(data_busca) != 6:
            print("Formato de data invalido")
            continue
        break
    while True:
        aday = input("Insira a data de fim do intervalo (formato mmddYY): ")
        aday = aday.replace("/", "")
        aday = aday.replace(" ", "")
        if int(aday[0:2]) > 12:
            print("Mes invalido")
            continue
        elif int(aday[2:4]) >= 32:
            print("Dia invalido")
            continue
        elif (int(aday[0:2]) == 2) and (int(aday[2:4]) > 30):
            print("Dia invalido")
            continue
        elif len(aday) != 6:
            print("Formato de data invalido")
            continue
        break

    if int(data_busca[4:]) > int(aday[4:]):
        print('Datas invalidas. 1')
        continue
    elif (int(data_busca[:2]) > int(aday[:2])):
        print('Datas invalidas. 2')
        continue
    elif (int(data_busca[:2]) == int(aday[:2])) and (int(data_busca[2:4]) > int(aday[2:4])):
        print('Datas invalidas. 3')
        continue
    else:
        break

print("-------------------------------------------------------------------------------------")
time.sleep(2)
print("OK! Não se assuste vamos lá! Jájá chega o email em...")
print("-------------------------------------------------------------------------------------")
time.sleep(5)

#ListaEmails.append(email_desejado)
#ListaEmails = [num for num in reversed(ListaEmails)
result_busca = bot_web_scraping.web_sc(sw_sch, data_busca, aday)

felps_gel = bot_registro_excel.montaPlanilha(result_busca)

bot_envio_email.send_email(ListaEmails, felps_gel)

print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("------------------------ PRONTO :) Confira lá no seu email ! ------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")