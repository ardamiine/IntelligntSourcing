from scrapy import Selector
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def findClass(x):
    if x=="dissolution_date":
        return "dissolution date"
    elif x=="registered_address":
        return "registered_address adr"
    elif 'inactive_directors' in x:
        return "officers trunc8"
    elif 'directors_/_officers' in x:
        return "officers trunc8"
    else:
        return x

def opencorporates(x):
    options=Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--disable-popup-blocking')
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://opencorporates.com/companies/dk/{x}")


    xpath = "/html/body[@class='companies']/div[@id='page_container']/div[@class='row content main_content']/div[@class='span7']/div[@class='vcard']/h1[@class='wrapping_heading fn org']"

    # Wait for the element to be present
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    print("Element found:", element.text)

    page=driver.page_source
    driver.quit()
    s=Selector(text=page)
    dt=s.xpath(".//dl[@class='attributes dl-horizontal']//dt//text()").extract()
    print(dt)
    dd=s.xpath(".//dl[@class='attributes dl-horizontal']//dd//text()").extract()
    d={i:"".join(s.xpath(f".//dl[@class='attributes dl-horizontal']//dd[@class='{findClass(i.lower().replace(' ', '_'))}']//text()").extract()) for i in dt}
    driver.quit()
    return d

if __name__=="__main__":
    list  = opencorporates("41401971")
    print(list)