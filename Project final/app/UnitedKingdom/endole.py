# https://suite.endole.co.uk/insight/search/?q=CHECKMATE+NEW+HOME+WARRANTY+LIMITED
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from scrapy import Selector
from bs4 import BeautifulSoup
import json
import time
from .tes import boomb

# Function to get page source using Selenium
def get_html_with_selenium(url, driver):
    driver.get(url)
    html = driver.page_source
    return html


# Main function to perform the scraping and saving
def endole(Name):
    Name = Name.replace(' ','+')
    base_url = "https://suite.endole.co.uk/insight/search/?q={}"
    
    options = Options()
    options.add_extension(r"C:\Users\amine.ardhaoui\Desktop\Intellegent sourcing V1\Project final\app\UnitedKingdom\buster.crx")
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    try:
        url = base_url.format(Name)
        html = get_html_with_selenium(url, driver)
        selector = Selector(text=html)
        status = selector.xpath("/html/body/div[4]/div[6]/div[2]/div[1]/div[5]/div[2]/div[2]/span/text()").get()
        contact = selector.xpath("/html/body/div[4]/div[6]/div[2]/div[2]/div[3]/table").get()
        totalAssets = selector.xpath("/html/body/div[4]/div[6]/div[3]/div[1]/div[4]/div[2]/span[2]").get()
        CreationDate = selector.xpath("/html/body/div[4]/div[6]/div[2]/div[1]/div[6]/div[2]/div[2]/text()").get()
        totalAssets = BeautifulSoup(totalAssets, 'html.parser').get_text()
        boomb()
    except:

        url = base_url.format(Name)
        html = get_html_with_selenium(url, driver)
        selector = Selector(text=html)
        status = selector.xpath("/html/body/div[4]/div[6]/div[2]/div[1]/div[5]/div[2]/div[2]/span/text()").get()
        contact = selector.xpath("/html/body/div[4]/div[6]/div[2]/div[2]/div[3]/table").get()
        totalAssets = selector.xpath("/html/body/div[4]/div[6]/div[3]/div[1]/div[4]/div[2]/span[2]").get()
        CreationDate = selector.xpath("/html/body/div[4]/div[6]/div[2]/div[1]/div[6]/div[2]/div[2]/text()").get()
        

    totalAssets = BeautifulSoup(totalAssets, 'html.parser').get_text()    
    contact = html_table_to_json(f'"""{contact}"""')
        
    
    
    return status,CreationDate,totalAssets,contact





def html_table_to_json(html_table):
    # Parse the HTML content
    soup = BeautifulSoup(html_table, 'html.parser')
    
    # Find all rows in the table
    rows = soup.find_all('tr')
    
    # Initialize an empty dictionary to store the key-value pairs
    table_data = {}
    
    for row in rows:
        # Extract the columns in each row
        cols = row.find_all('td')
        
        # Only process rows with at least two columns
        if len(cols) > 1:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            table_data[key] = value
    
    # Convert dictionary to JSON string
    json_data = json.dumps(table_data, indent=4)
    
    return json_data


#captcha

def captcha(driver):
    time.sleep(2)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
    driver.implicitly_wait(5)
    driver.switch_to.default_content()
    iframe = driver.find_element(By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')
    driver.switch_to.frame(iframe)
    try:
        driver.find_element(By.XPATH,'//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]').click()
        time.sleep(2)
    except:
        pass
    driver.switch_to.default_content()
    time.sleep(2)
    
    


if __name__ == "__main__":
    status,CreationDate,totalAssets,contact = endole("03718331")
    print(status,totalAssets,CreationDate)
    #exemple
    print("\n-----------",contact,"\n--------------")
    contact = json.loads(contact)

    print("Registered Address : ",contact.get("Registered Address"))
    