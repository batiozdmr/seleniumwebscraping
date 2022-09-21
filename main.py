import datetime
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def chrom_set():
    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return chrome_driver


baslik = input("hangi başlığı aramak istiyorsunuz?\n")
url = "https://www.eksisozluk.com"
columns = [
    'Icerik',
    'Yazar',
    'Tarih',
    'Konu',
]
rows = [columns]
browser = chrom_set()
time.sleep(3)
browser.get(url)
time.sleep(3)
input_area = browser.find_element(By.ID, "search-textbox")
button = browser.find_element(By.XPATH, "//form[@id='search-form']/button[1]")
time.sleep(3)
input_area.send_keys(baslik)
time.sleep(2)
button.click()
time.sleep(3)
url = browser.current_url
source = browser.page_source
soup = BeautifulSoup(source, "html.parser")
try:
    page_count = len(
        soup.find("div", {"class": "clearfix sub-title-container"}).find("div", {"class": "pager"}).find_all("option"))
except:
    page_count = 1

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
for i in range(1, page_count + 1):
    response = requests.get(url + "?p=" + str(i), headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(response.content, "html.parser")
    entry_divs = soup.find_all("div", {"class": "content"})
    for entry in entry_divs:
        footer = entry.findNext("footer")
        author = footer.find_all("a")[0].text
        date = footer.find_all("a")[1].text
        rows.append((
            entry.text,
            author,
            date,
            baslik,
        ))

df = pd.DataFrame(rows)
now_time = datetime.datetime.now()
writer_b = pd.ExcelWriter('rapor-' + str(baslik) + '-' + str(now_time.date()) + '.xlsx', engine='xlsxwriter')
df.to_excel(writer_b, sheet_name=str(now_time.date()), index=False)
writer_b.save()
browser.close()
