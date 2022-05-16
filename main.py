import bot_web_scraping
import bot_envio_email

print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("----- Ola! Para obter os dados sobre a vulnerabilidade siga os passos a seguir. -----")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
ListaEmails = [
    
]
#'gelsinhomusico@gmail.com',
#    '2.gelsinhomusico@gmail.com',

while True:
    email_desejado = input("Primeiro digite o email para onde enviaremos os resultados: ")
    if ('@' not in email_desejado) or ('.' not in email_desejado):
        print('Email invalido, por gentileza digite novamente.')
        continue
    else:
        break
ListaEmails.append(email_desejado)
ListaEmails = [num for num in reversed(ListaEmails)]

bot_envio_email.send_email(ListaEmails, bot_web_scraping.dados_monta_email)
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("------------------------ PRONTO :) Confira lá no seu email ! ------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")