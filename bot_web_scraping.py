import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from bs4 import BeautifulSoup
import requests
import re
import json

#from cgitb import text
#import pandas as pd
# import numpy as np
#from openpyxl import load_workbook
#from openpyxl.styles import Alignment
#from openpyxl.styles import Font
# from openpyxl.styles import PatternFill

#import bot_registro_excel


def web_sc(sw_sch, data_busca, aday):
    

    # * Apontamento do diretorio onde está o driver do Chrome (versão 101 dos navegadores).
    # * Logo mais é iniciado o Webdriver utilizando o driver especificado.
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(PATH,chrome_options=options)
    today = date.today() # * Data de hoje.
    # * Site para coleta de dados
    driver.get("https://nvd.nist.gov/vuln/search")
    #TODO: Na integração substituir as variaveis por valores de input
    #TODO: Adicionar verificador do status do site para evitar crashs (com a biblioteca requests)
    try:
        #* Função para buscar a localização do botão  que muda para modo "Advanced"
        #* Foi utilizado funções da biblioteca Selenium Webdriver para localizar o botão.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "SearchTypeAdvanced"))
        )    
        element.click() #* Método que clica automaticamente no local especificado na variavel "element".
        #####
        #* Localizando o campo de data inicial da busca.
        #TODO: Insirir limitador para periodos de até 120 dias.
        inp_date = driver.find_element(By.ID,"published-start-date")   
        inp_date.send_keys(data_busca)  #* Método que insere a data no campo especificado.
        #####
        inp_date = driver.find_element(By.ID, "published-end-date")
        # aday = today.strftime("%m%d%Y") #* Utilizando a biblioteca "datetime" para inserir a data atual do PC.
        inp_date.send_keys(aday)
        
        #####
        #* Inserindo o software a ser pesquisado. 
        inp_sw = driver.find_element(By.ID, "Keywords")
        inp_sw.send_keys(sw_sch)
        #####
        #* Apertando o botão de "Search".
        #? Seria bom tratar erros na busca? (Ex.: Periodo maior que 120 dias)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "vuln-search-submit"))
        )
        element.click()
        #####
        #TODO: Verificar se a linha abaixo é necessaria.
        url_n = driver.current_url
        #####
        #! A partir desse momento será utilizando muito mais o BeautifulSoup para tratar a HTML e o requests para acessar elas.
        #* Usando o Requests para baixar a HTML e o Soup para "tratar" ela.
        response = requests.get(url_n)
        content_t = response.content
        site_t = BeautifulSoup(content_t, 'html.parser')
        num_vuln = site_t.find(attrs={"data-testid": "vuln-matching-records-count"})
        num_vuln = int(str(num_vuln.contents)[2:-2])
        #print(type(num_vuln))
        num_pg = []
        lst_felps = []
        if num_vuln > 20:
            for busca in site_t.find_all(attrs={"aria-label": re.compile('Page')}):
                if ("https://nvd.nist.gov"+str(busca["href"])) in num_pg:
                    continue
                elif '&gt' in str(busca["href"]):
                    continue
                else:
                    num_pg.append("https://nvd.nist.gov"+str(busca["href"]))
        else:
            num_pg.append(url_n)
        #print("Paginas: ",num_pg)
        for pg_b in num_pg:
            response = requests.get(pg_b)
            content_t = response.content
            site_t = BeautifulSoup(content_t, 'html.parser')
            #####
            #* O for foi utilizado para localizar todos os <a> da HTML e a frente serão selecionados aqueles que possuem o termo "CVE"
            for link in site_t.find_all('a'):
                refadv = []
                severity = []
                src_lst = []
                cpe_cd = []
                publi_d = ''
                sub_lst = []
                if 'CVE' in str(link.contents):
                    #* Os links contidos na variavel localizada estavam incompletos, sendo necessario concatenar as str e gerar novo link.
                    new_link = "https://nvd.nist.gov" + str(link.get('href'))
                    driver.get(new_link)
                    cont_new = requests.get(new_link)
                    cont_new_t = cont_new.content
                    site_n_t = BeautifulSoup(cont_new_t, 'html.parser')
                    #print(site_n_t.prettify())
                    #####
                    #* Utilizando método find do BS para localizar o código CVE, armazenado na variavel cve_cd.
                    cve_cd = site_n_t.find(attrs = {'data-testid':'page-header-vuln-id'})
                    cve_cd = str(cve_cd.contents)[1:-1] #* Retirado caracteres a mais.
                    #####
                    #* Mesmo modelo utilizado anterior mente agora para loclaizar a descrição.
                    descrit = site_n_t.find('p', attrs={'data-testid': 'vuln-description'})
                    descrit = str(descrit.contents)[1:-1]
                    #####
                    #* Utilizando o método "find_all" do BS para localizar os graus de severidade anotados da vunerabilidade.
                    for busca in site_n_t.find_all(attrs={'id': re.compile('Cvss3')}):
                        if 'Cna' in busca['id']:
                            severity.append((str(busca.contents)[2:-2]) + ' (CNA)') 
                            #? Verificar se é possivel identificar cada uma das notas]
                        else:
                            severity.append((str(busca.contents)[2:-2]) + ' (NIST)') 
                    
                    #####
                    #* Mesmo principio porem agora para localizar links de esclarecimento do fornecedor do software
                    #* OBS.: Foi utilizado a biblioteca re junto com métodos compile para localizar de maneria geral palavras
                    #* que contenham a parte já especificada (inserido palavra parcial)
                    for busca in site_n_t.find_all(attrs= {'data-testid' : re.compile("vuln-hyperlinks-link-")}):
                        refadv.append(busca.text)
                    
                    #####
                    #* Iniciando com try pois existem casos em que não é especificado o código "CPE" e quando ocorria o sw bugava.
                    try:
                        #####
                        #* Localizado a linha do HTML com json(s) inserido(s).
                        for busca in site_n_t.find_all('input', attrs= {'id' : re.compile("cveTreeJsonDataHidden")}):
                            tens = busca
                        
                        #####
                        #* Retirado o(s) json da linha do HTML e feito o split para casos em que há mais de um json.
                        js_part = tens['value'][1:-1].split("[]}]}]},")
                        #####
                        #* Elaborado lista com os json corrigidos após o split.
                        for ptr in range(0,len(js_part)):
                            if ptr == len(js_part)-1:
                                src_lst.append(js_part[ptr])
                            else:
                                src_lst.append(js_part[ptr]+"[]}]}]}")
                        
                        #####
                        #* Utilizado a biblioteca json + método loads para converter ele em um dicionario e ser tratado no codigo.
                        for rg in range(0,len(src_lst)):
                            scr = json.loads(src_lst[rg])
                            cpe_cd.append(scr["containers"][0]["containers"][0]["cpes"][0]["cpe23Uri"]) #? Seria possivel melhorar?
                            #? Esse levantamento foi feito com base no padrão da loclaização da informação, mas está muito "truncado"                    
                    except:
                        cpe_cd.append("None")
                    #####
                    #* Mesma logica já utilizado para localizar conteudo com palavras parciais, agora para localizar a data de publicação.
                    for busca in site_n_t.find_all(attrs= {'data-testid' : re.compile("vuln-published-on")}):
                        publi_d = str(busca.contents)
                    sub_lst.append(sw_sch)
                    sub_lst.append(cve_cd)
                    #print("Código CVE: ", cve_cd)
                    sub_lst.append(descrit)
                    #print("Descrição: ", descrit)
                    sub_lst.append(severity)
                    #print("Severidade: ", severity)
                    sub_lst.append(refadv)
                    #print("Referencia: ", refadv)
                    sub_lst.append(cpe_cd)
                    #print("Código CPE: ", cpe_cd)
                    sub_lst.append(publi_d)
                    #print("Data de publicação: ", publi_d)
                    sub_lst.append(new_link)
                    #print("Site da CVE", new_link)
                    #print(sub_lst)
                    lst_felps.append(sub_lst)
                    #time.sleep(1)
                    driver.back()
            #####
            ######
        #time.sleep(2)
    except:
        driver.quit()

    driver.close()

    #dados_monta_email = bot_registro_excel.montaPlanilha(lst_felps)
    #print(lst_felps)
    return(lst_felps)

