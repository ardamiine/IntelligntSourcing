

# This code is for scraping the Statstidende site (Denmark court site)
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from scrapy import Selector
import time

def auktioner(Num_CVR):
    base_url = "https://auktioner.dk/konkurser/?q={}&aarbagud=alle&sortering=Cvrnr&retning=Stigende&side=1"
    base_u = "https://auktioner.dk"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    url = base_url.format(Num_CVR)
    driver.get(url)
    html = driver.page_source
    selector = Selector(text=html)
    href_value = selector.xpath("/html/body/form/div[6]/div[3]/div/table/tbody/tr[2]/td[3]/a/@href").get()
    try:
        driver.get(base_u+href_value)
        sleep(1)
        selector = Selector(text=driver.page_source)
    except:
        pass
    driver.quit()
    cleaned_texts=""
    try:
        h3_element = selector.xpath("//h3[text()='Kurator']")
        following_texts = h3_element.xpath("following-sibling::br/following-sibling::text()").getall()
        cleaned_texts = [text.strip() for text in following_texts]
        cleaned_texts=cleaned_texts[:cleaned_texts.index("")]
    except:
        pass
    try:
        a=selector.xpath("/html/body/form/div[6]/table/tbody/tr[5]/td[3]/text()").get()
        b=selector.xpath("/html/body/form/div[6]/table/tbody/tr[6]/td[3]/text()").get()
    except:
        pass

    return cleaned_texts,a,b
if __name__ == "__main__":
    print(auktioner("40828311"))