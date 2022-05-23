import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re
import json

#! Web Scraping V2 - Adaptado para rodar com interfacegrafica.
#todo Adicionar indicadores de falha de conexão.
def web_sc(sw_sch, data_busca, aday):
    
    # * Apontamento do diretorio onde está o driver do Chrome (versão 101 dos navegadores).
    # * Logo mais é iniciado o Webdriver utilizando o driver especificado.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    # * Site para coleta de dados
    driver.get("https://nvd.nist.gov/vuln/search")
    #TODO: Na integração substituir as variaveis por valores de input
    #TODO: Adicionar verificador do status do site para evitar crashs (com a biblioteca requests)
    results_fc = []
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
        lev_vuln = 0        
        num_vuln = int(str(num_vuln.contents)[2:-2])
        num_pg = []
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
        new_link = []
        for pg_b in num_pg:
            response = requests.get(pg_b)
            content_t = response.content
            site_t = BeautifulSoup(content_t, 'html.parser')
            #####
            #* O for foi utilizado para localizar todos os <a> da HTML e a frente serão selecionados aqueles que possuem o termo "CVE"
            
            for link in site_t.find_all('a'):            
                if 'CVE' in str(link.contents):
                    #* Os links contidos na variavel localizada estavam incompletos, sendo necessario concatenar as str e gerar novo link.
                    new_link.append("https://nvd.nist.gov" + str(link.get('href')))

        results_fc.append(0)
        results_fc.append(new_link)
        results_fc.append(num_vuln)
        return results_fc
    except:
        driver.quit()
        results_fc.append(-1)
        results_fc.append([-1])
        results_fc.append(0)
        return results_fc
        #Todo -------------------- Fim da primeira função --------------------
                
def web_cole(sw_sch, new_link = []):  
    refadv = []
    severity = []
    src_lst = []
    cpe_cd = []
    publi_d = ''
    sub_lst = []
    cont_new = requests.get(new_link)
    cont_new_t = cont_new.content
    site_n_t = BeautifulSoup(cont_new_t, 'html.parser')
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
            #? Esse levantamento foi feito com base no padrão da localização da informação, mas está muito "truncado"                    
    except:
        cpe_cd.append("None")
    #####
    #* Mesma logica já utilizado para localizar conteudo com palavras parciais, agora para localizar a data de publicação.
    for busca in site_n_t.find_all(attrs= {'data-testid' : re.compile("vuln-published-on")}):
        publi_d_pre = str(busca.contents)[2:-2]
        pb_m, pb_d, pb_y = publi_d_pre.split('/')
        publi_d = pb_d + '/' + pb_m + '/' + pb_y
    sub_lst.append(sw_sch)
    sub_lst.append(cve_cd)
    sub_lst.append(descrit)
    sub_lst.append(severity)
    sub_lst.append(refadv)
    sub_lst.append(cpe_cd)
    sub_lst.append(publi_d)
    sub_lst.append(new_link)
    return sub_lst

def auto_do(sw_sch_e = str, data_busca_e = str, aday_e = str):
    leitor = []
    leitor = web_sc(sw_sch_e, data_busca_e, aday_e)
    #print(leitor)
    dt_pes = []
    result_auto = []
    if leitor[0] == 0:
        print(len(leitor[1]))
        cnt = 0
        for i in range(0,len(leitor[1])):
            dt_pes.append(web_cole(sw_sch_e, leitor[1][i]))
            cnt += 1
            print(cnt)
        result_auto.append(0)
        result_auto.append(dt_pes)
        return result_auto
    else:
        result_auto.append(-1)
        result_auto.append([-1])
        return result_auto

#* Testes de validação versão 2
# sw_sch_e = 'opera'
# data_busca_e = '050322'
# aday_e = '051522'

# auto_do(sw_sch_e, data_busca_e, aday_e)