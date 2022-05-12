import os
import smtplib
from email.message import EmailMessage

sender = "g3.webscraping@gmail.com"
receiver = "gelsonfilho.contato@gmail.com"
password =  "OtGeFi252424@"
server = "smtp.gmail.com"
port = 465

#Configurar email, senha
EMAIL_ADDRESS = sender
EMAIL_PASSWORD = password

#Criar um email
msg = EmailMessage()

#Titulo
msg['Subject'] = 'titulo do email'

#Remetente
msg['From'] = EMAIL_ADDRESS

#Destinatário
msg['To'] = receiver

#Conteúdo do email
msg.set_content('------ Aqui está o conteúdo do email ------ ')

#Envia o email
with smtplib.SMTP_SSL(server, port) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)