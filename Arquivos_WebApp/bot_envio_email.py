import os
import smtplib
# import LoginData
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import pandas as pd
import pyAesCrypt



#* SMTP - Simple Mail transfer protocol
#* Para criar o servidor e enviar o email


nome_da_planilha = "VulnerabilidadesSolicitadas"

def send_email(lista_emails, dicionario):

    #!-------------------------------------------------------------------------------------------------------------
    #!1 - Inicia servidor
    #!-------------------------------------------------------------------------------------------------------------
    bufferSize = 64 * 1024
    password = " r@nd0m5enh@12345"
    encFileSize = os.stat("LoginData.AES_G3WSware").st_size
    with open("LoginData.AES_G3WSware", "rb") as fIn:
        try:
            with open("LoginData.py", "wb") as fOut:
                pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
        except ValueError:
            print ('senha incorreta')
    import LoginData
    host = LoginData.host
    port = LoginData.port
    login = LoginData.login
    password = LoginData.password
    os.remove("LoginData.py")
    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(login, password)


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
        corpo_email_2 = ""
        if(int(df.shape[0]) > 20):
            corpo_email_2 = "A quantidade de vulnerabilidade críticas ou altas é superior a 20. Verificar demais resultados no anexo."

        corpo_email = df.to_html(index=False,justify="center",render_links=True,max_rows=20) #converte para html
        corpo_email = corpo_email.replace("[","").replace("]","").replace(", "," - ").replace("'","")
        corpo_email = corpo_email.replace("HIGH","'High'").replace("MEDIUM","'Medium'").replace("CRITICAL","'Critical'").replace("LOW","'Low'")
        corpo_email = corpo_email.replace("<tr style=\"text-align: center;\">","<tr style=\"text-align: center;\" bgcolor=\"DimGray\">")
        corpo_email = corpo_email.replace("<tr>","<tr style=\"text-align: center;\">")
        corpo_email = corpo_email.replace("<th>Software/Sistema</th>","<th><font color=\"White\"> Software/Sistema </font></th>")
        corpo_email = corpo_email.replace("<th>CVE</th>","<th><font color=\"White\"> CVE </font></th>")
        corpo_email = corpo_email.replace("<th>Severidade</th>","<th><font color=\"White\"> Severidade </font></th>")
        corpo_email = corpo_email.replace("<th>Data de publicação NVD</th>","<th><font color=\"White\"> Data de publicação NVD </font></th>")
        corpo_email = corpo_email.replace("<th>Link CVE</th>","<th><font color=\"White\"> Link CVE </font></th>")
        corpo_email = corpo_email.replace("'High'","<font color=\"Orange\">'High'</font>")
        corpo_email = corpo_email.replace("'Critical'","<font color=\"Red\">'Critical'</font>")

        email_msg = MIMEMultipart()
        email_msg['Subject'] = 'Vulnerabilidades Críticas Data '+ datetime.today().strftime("%Y-%m-%d %H:%M:%S") #pega a data atual
        email_msg['From'] = login
        email_msg['To'] = email_destinatario
        email_msg.attach(MIMEText("Abaixo está uma tabela apenas com as CVE's cuja as severidades foram dadas como altas/críticas por pelo um dos padrões CVSS Versão 3.x (NIST ou CNA). Em anexo, segue planilha do excel com dados completos solicitados independente da severidade.",'Plain'))
        email_msg.attach(MIMEText(corpo_email,'html'))
        email_msg.attach(MIMEText(corpo_email_2,'Plain'))

        # print("----------------------------------------")
        # print("----------------------------------------")
        # print(corpo_email)
        # print("----------------------------------------")
        # print("----------------------------------------")

        #!-------------------------------------------------------------------------------------------------------------
        #!3 - Inserção de anexo
        #!-------------------------------------------------------------------------------------------------------------

        #Abre o arquivo em modo leitura e binary
        # path_file_attach = os.path.dirname(os.path.realpath(__file__)) + "\\" + nome_da_planilha + ".xlsx"
        # attchment = open(path_file_attach, 'rb')
        attchment = open('VulnerabilidadesSolicitadas.xlsx', 'rb')

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

        #todo -------------------- cria a planilha html para uso posterior do bot_whatsapp se preciso
        f = open('planilha.html','w')
        f.write(corpo_email)
        f.close()

        #!-------------------------------------------------------------------------------------------------------------
        #!4 - Envia o email tipo MIME no SERVIDOR SMTP
        #!-------------------------------------------------------------------------------------------------------------
        server.sendmail(email_msg['From'],email_msg['To'],email_msg.as_string())
    

    #!Encerra o servidor
    server.quit()


