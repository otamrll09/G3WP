import os
from selenium import webdriver
import time
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
import aspose.words as aw

def send_wpp(numero,software_pesquisado):

    if not(numero == ""):
        doc = aw.Document(os.path.dirname(os.path.realpath(__file__)) + "\\planilha.html")
        doc.save("Planilha.txt")
        with open('Planilha.txt', 'r') as arquivo:
            string_planilha = arquivo.read().replace(software_pesquisado,"\n").replace("publicaÃ§Ã£o","publicação").replace("Link CVE","Link CVE\n--------------------").replace("ï»¿","").replace('Evaluation Only. Created with Aspose.Words. Copyright 2003-2022 Aspose Pty Ltd.', 'Ordem dos ítens:\n').replace("Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/","")

        nome_da_planilha = "VulnerabilidadesSolicitadas"
        path_file_attach_xlsx = os.path.dirname(os.path.realpath(__file__)) + "\\" + nome_da_planilha + ".xlsx"

        #!Manda para o whatsapp a mesma planilha
        hname = str(os.getlogin())
        CHROME_PROFILE_PATH = "user-data-dir=C:\\Users" + "\\"+ hname + "\\" + "AppData\\Local\\Google\\Chrome\\User Data\\Default"
        PATH = os.path.dirname(os.path.realpath(__file__)) + "\\" + "chromedriver.exe"
        # PATH = 'C:\Program Files (x86)\chromedriver.exe'
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument(CHROME_PROFILE_PATH)
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        driver = webdriver.Chrome(executable_path=PATH,options=options)
        # driver = webdriver.Chrome(executable_path=PATH)
        # texto = urllib.parse.quote("Ola! teste teste")
        texto = urllib.parse.quote(f"Ola! Você pesquisou por: *{software_pesquisado}*. Segue em anexo a planilha com todos os resultados encontrados e abaixo apenas os resultados de vulnerabilidades altas e/ou críticas! Isso também foi enviado para os emails solicitados :)\n--------------------\n"+string_planilha)
        # link = "https://web.whatsapp.com/send?phone=+5515996512099&text={texto}"
        link = "https://web.whatsapp.com/send?phone=+55" + numero + f"&text={texto}"
        driver.get(link)
        # time.sleep(2)
        #---------------- clica em enter na mensagem de texto
        while len(driver.find_elements(By.CSS_SELECTOR, value="span[data-icon='send']")) < 1:
            time.sleep(1)
        time.sleep(1)
        send = driver.find_element(By.CSS_SELECTOR, value="span[data-icon='send']").click()  
        #---------------- procura o clip onde insere anexo
        while len(driver.find_elements(By.CSS_SELECTOR, value="span[data-icon='clip']")) < 1:
            time.sleep(1)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, value="span[data-icon='clip']").click()
        #---------------- seleciona o anexo
        while len(driver.find_elements(By.CSS_SELECTOR, value="input[type='file']")) < 1:
            time.sleep(1)
        time.sleep(1)
        attach = driver.find_element(By.CSS_SELECTOR, value="input[type='file']")
        attach.send_keys(path_file_attach_xlsx)
        #---------------- clica em enviar anexo
        while len(driver.find_elements(By.CSS_SELECTOR, value="span[data-icon='send']")) < 1:
            time.sleep(1)
        time.sleep(1)
        send = driver.find_element(By.CSS_SELECTOR, value="span[data-icon='send']")
        send.click()  
        time.sleep(3)
        driver.quit()        

    path1 = os.path.dirname(os.path.realpath(__file__)) + "\\" + "VulnerabilidadesSolicitadas.xlsx"
    path2 = os.path.dirname(os.path.realpath(__file__)) + "\\" + "planilha.html"
    path3 = os.path.dirname(os.path.realpath(__file__)) + "\\" + "Planilha.txt"
    if os.path.isfile(path1):
        os.remove(path1)
    if os.path.isfile(path2):
        os.remove(path2)
    if os.path.isfile(path3):
        os.remove(path3)