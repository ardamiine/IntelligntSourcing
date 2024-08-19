from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
from selenium.webdriver.common.action_chains import ActionChains
 
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
 
 
def boomb():
    options = webdriver.ChromeOptions()
    options.add_extension(r"C:\Users\amine.ardhaoui\Desktop\Intellegent sourcing V1\Project final\app\UnitedKingdom\buster.crx")
    #options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-search-engine-choice-screen")
    driver=webdriver.Chrome(options=options)
    driver.get("https://www.endole.co.uk/backend/unblock-ip/?URI=https://suite.endole.co.uk%2Finsight%2Fsearch%2F%3Fq%3D")
    time.sleep(2)
    captcha(driver)
    driver.execute_script('document.querySelector("body > div:nth-child(2) > div:nth-child(1) > form > input[type=submit]:nth-child(4)").click();')
    time.sleep(2)
    driver.close()

if __name__== "__main__":
   boomb()