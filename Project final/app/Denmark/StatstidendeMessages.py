# This code is for scraping the Statstidende site (Denmark court site)
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from scrapy import Selector
from tools import convert_to_df, translate_to_en, save_to_excel
from bs4 import BeautifulSoup

# Function to get page source using Selenium
def get_html_with_selenium(url, driver):
    driver.get(url)
    sleep(5)  # Give time for the page to fully load (adjust as needed)
    html = driver.page_source
    return html


# Main function to perform the scraping and saving
def statstidendemessages(CVR):
    base_url = "https://www.statstidende.dk/messages?t={}&toDate"
    all_data = pd.DataFrame()
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    try:
        url = base_url.format(CVR)
        html = get_html_with_selenium(url, driver)
        selector = Selector(text=html)
        MessageId = selector.xpath("/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[4]/div[1]/div[1]/div[2]/text()").get()
        print(MessageId)
        url2 = f"https://www.statstidende.dk/messages/{MessageId}"
        html2 = get_html_with_selenium(url2, driver)
        selector2 = Selector(text=html2)
        rapport = selector2.xpath("/html/body/div/div/div/div[2]/div/div[1]/div/div[3]/div").get()
        rapport = BeautifulSoup(rapport, 'lxml')
        rapport = rapport.getText()
        curator = selector2.xpath("/html/body/div/div/div/div[2]/div/div[1]/div/div[3]/div/div[4]").get()
        curator = BeautifulSoup(curator, 'lxml')
        curator = curator.getText()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return rapport,curator

if __name__ == "__main__":
    Rapport,Curator = statstidendemessages("41401974")
    print(Curator)