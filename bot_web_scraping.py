from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
from bs4 import BeautifulSoup
import requests

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
today = date.today()

driver.get("https://nvd.nist.gov/vuln/search")
data_busca = "03052022"
sw_sch = "microsoft"

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "SearchTypeAdvanced"))
    )
    element.click()
    inp_date = driver.find_element_by_id("published-start-date")
    inp_date.send_keys(data_busca)

    inp_date = driver.find_element_by_id("published-end-date")
    aday = today.strftime("%m%d%Y")
    inp_date.send_keys(aday)
    
    inp_sw = driver.find_element_by_id("Keywords")
    inp_sw.send_keys(sw_sch)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "vuln-search-submit"))
    )
    element.click()
    url_n = driver.current_url
    response = requests.get(url_n)
    content_t = response.content
    print(url_n)
    site_t = BeautifulSoup(content_t, 'html.parser')
    print(site_t.prettify())
    #srch_w = driver.find_element(By.CLASS_NAME, "vuln-detail-link-0")
    #print(srch_w)
    #driver.get("https://nvd.nist.gov/vuln/search")

    time.sleep(5)
except:
    driver.quit()
