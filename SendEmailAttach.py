import os
import smtplib
import LoginData
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import pandas as pd
#* SMTP - Simple Mail transfer protocol
#* Para criar o servidor e enviar o email


def send_email(lista_emails, dicionario, nome_da_planilha):
    #!-------------------------------------------------------------------------------------------------------------
    #!1 - Inicia servidor
    #!-------------------------------------------------------------------------------------------------------------
    server = smtplib.SMTP(LoginData.host, LoginData.port)
    server.ehlo()
    server.starttls()
    server.login(LoginData.login, LoginData.password)


    #!1 - Laço FOR para enviar para mais de um email
    for email_destinatario in lista_emails:

        #!-------------------------------------------------------------------------------------------------------------
        #!2 - Constroi o email tipo MIME -- texto
        #!-------------------------------------------------------------------------------------------------------------
        df = pd.DataFrame(dicionario)
        df = df.drop(columns=['Current Description']) #tirando a coluna
        df = df.drop(columns=['References to Advisories, Solutions, and Tools']) #tirando a coluna
        df = df.drop(columns=['Known Affected Software Configurations']) #tirando a coluna
        df = df[df['Severity']>=7] #selecionando apenas os com severidade grave (que é os maiores q 7)
        corpo_email = df.to_html(bold_rows=True,index=False,justify="center",render_links=True) #converte para html

        email_msg = MIMEMultipart()
        email_msg['Subject'] = 'Vulnerabilidades Críticas Data '+ datetime.today().strftime('%d/%m/%Y') #pega a data atual
        email_msg['From'] = LoginData.login
        email_msg['To'] = email_destinatario
        email_msg.attach(MIMEText(corpo_email,'html'))


        #!-------------------------------------------------------------------------------------------------------------
        #!3 - Inserção de anexo
        #!-------------------------------------------------------------------------------------------------------------

        #Abre o arquivo em modo leitura e binary
        path_file_attach = os.path.dirname(os.path.realpath(__file__)) + "\\" + nome_da_planilha + ".xlsx"
        attchment = open(path_file_attach, 'rb')

        #Lê o arquivo em modo binário e coloca ele no email codificado em base 64 (que é o que o email precisa)
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attchment.read())
        encoders.encode_base64(att)

        #Adiciona o cabeçalho no tipo anexo de email
        att.add_header('Content-Disposition',f'attachment; filename={nome_da_planilha}.xlsx')

        #fecha o arquivo
        attchment.close()

        #insere no corpo do email
        email_msg.attach(att)



        #!-------------------------------------------------------------------------------------------------------------
        #!4 - Envia o email tipo MIME no SERVIDOR SMTP
        #!-------------------------------------------------------------------------------------------------------------
        server.sendmail(email_msg['From'],email_msg['To'],email_msg.as_string())
    

    #!Encerra o servidor
    server.quit()



