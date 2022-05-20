import os
from selenium import webdriver
import time
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By

def send_wpp(numero):
    if not(numero == ""):
        nome_da_planilha = "VulnerabilidadesSolicitadas"
        path_file_attach = os.path.dirname(os.path.realpath(__file__)) + "\\" + nome_da_planilha + ".xlsx"

        #!Manda para o whatsapp a mesma planilha
        CHROME_PROFILE_PATH = "user-data-dir=C:\\Users\\lenovo\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        PATH = 'C:\Program Files (x86)\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(CHROME_PROFILE_PATH)
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        driver = webdriver.Chrome(executable_path=PATH,options=options)
        texto = urllib.parse.quote(f"Ola! Aqui está a planilha com todos os resultados encontrados! No seu email, enviamos esta mesma planilha. Lá destacamos as CVEs críticas ou altas no corpo email para você ter um overview mais genérico :)")
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
        attach.send_keys(path_file_attach)
        #---------------- clica em enviar anexo
        while len(driver.find_elements(By.CSS_SELECTOR, value="span[data-icon='send']")) < 1:
            time.sleep(1)
        time.sleep(1)
        send = driver.find_element(By.CSS_SELECTOR, value="span[data-icon='send']")
        send.click()  
        time.sleep(3)
        driver.quit()        

#!criar um arquivo html e mandar tbm com os resultados só com os criticos/high e tal