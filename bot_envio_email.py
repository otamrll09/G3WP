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


nome_da_planilha = "VulnerabilidadesSolicitadas"

def send_email(lista_emails, dicionario):
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
        df = df.drop(columns=['Descrição']) #tirando a coluna
        df = df.drop(columns=['Referências para recomendações, soluções e ferramentas']) #tirando a coluna
        df = df.drop(columns=['Configurações de softwares afetadas']) #tirando a coluna

        #todo aqui embaixo, neste grupo, eu verifico quais itens da severidade possuem valor menor q 7 e excluo suas linhas do q ira no corpo do email
        dicionario_severidades = df.to_dict()['Severidade']
        indices_para_excluir = []
        indice = 0
        for i in list(dicionario_severidades.values()):
            if len(i) == 1:
                if(i[0].__contains__("N/A")):
                    indices_para_excluir.append(indice)
                elif float(i[0][:3]) < 7:
                    indices_para_excluir.append(indice)
            else:
                if( (not(i[0].__contains__("N/A"))) and (not(i[1].__contains__("N/A"))) ):
                    if (float(i[0][:3]) < 7) and (float(i[1][:3]) < 7):
                        indices_para_excluir.append(indice)
                elif( (not(i[0].__contains__("N/A"))) and (i[1].__contains__("N/A")) ):
                    if float(i[0][:3]) < 7:
                        indices_para_excluir.append(indice)
                elif( (i[0].__contains__("N/A")) and (not(i[1].__contains__("N/A"))) ):
                    if float(i[1][:3]) < 7:
                        indices_para_excluir.append(indice)
                else: #caso os dois baseScore-cvss forem N/A
                    indices_para_excluir.append(indice)
            indice += 1
        for i in indices_para_excluir:
            df = df.drop(i)
        #todo termina aqui essa lógica para exclusao  -----------------------------------------------------------------------------------------------

        corpo_email = df.to_html(index=False,justify="center",render_links=True) #converte para html

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


