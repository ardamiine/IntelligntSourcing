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


# Function to get page source using Selenium
def get_html_with_selenium(url, driver):
    driver.get(url)
    sleep(5)  # Give time for the page to fully load (adjust as needed)
    html = driver.page_source
    return html

# Function to extract information from the HTML using XPath
def get_info(selector):
    items = selector.xpath("//div[@class='message-entry py-3 pl-sm-0 container']")
    
    all_info = []
    for item in items:
        title = item.xpath(".//div[@class='message-number']/text()").get()
        company_name = item.xpath(".//a/h3[@class='pt-2 pt-sm-0']/text()").get()
        num_cvr = item.xpath(".//div[@class='message-summary'][1]/div/text()").get()
        court_district = item.xpath(".//div[@class='message-summary'][1]/div[2]/text()").get()
        date_annonce = item.xpath(".//div[@class='message-summary'][2]/div[@class='message-date']/text()").get()
        
        info = {
            "Court Message": translate_to_en(title.strip() if title else ''),
            "Company Name": company_name.strip() if company_name else '',
            "N° CVR": num_cvr.replace("CVR-nr.: ", "").strip() if num_cvr else '',
            "Court District": court_district.replace("Retskreds: ", "").strip() if court_district else '',
            "DateAnnonce": date_annonce.replace("Kundgørelsesdato: ", "").strip() if date_annonce else '',


        }
        all_info.append(info)
        print(info)
    
    return all_info
# Main function to perform the scraping and saving
def statstidende(StartDate,EndDate):
    base_url = "https://www.statstidende.dk/messages?fromDate={}T00%3A00%3A00&j=b6be885d-f058-4299-b2ca-dc7ca4ca104b&j=deb3692c-68dc-4e28-9ee2-8a4b7a452c05&j=fd012bb9-1b23-46d1-8f20-06fb03dbe8b4&j=daa6d232-8050-4e42-96a8-ffb57eb51cb2&j=399501aa-d9ca-4859-bc5b-e89b19ca2219&j=78ae3ae6-b57a-49ba-843e-cc2d55a2b789&j=63595023-f352-4844-b8c1-7a10e9bf700d&j=52a359ec-1839-487d-8966-52ae39b7c820&j=37776d37-ebcd-4d3f-96ea-de4e1d41a4fe&j=da4835b1-d33d-48d8-8249-3c7915a4c948&j=1277d0d0-6cd6-4f8d-9b92-3e99c9220caf&j=72dd6e65-ba98-446e-8f64-0280e714b8dc&j=d5f74d61-2673-4746-9f18-f11033823795&j=86db09b0-e2a6-42bd-99b3-4596371d822e&j=e767bcf4-a903-42fd-96f1-d870ed2324a8&j=84ba8198-d5f9-493f-8732-0ad55c6aeb59&j=7cad6f39-316f-4adc-9c1c-5bddc5a9996f&j=90902773-a16b-4efc-aba1-d49d6fe29cb2&j=ce9b08cd-fd5d-4b4f-9375-780c2ec2743a&j=0d695786-439d-4d9f-8b8e-490c7115e54f&j=35ccc623-0494-4fac-a061-8cab7607bff7&j=ecb504f6-3574-40e0-910c-d4e158f4d33d&j=df7354d9-910f-4a7b-8b0f-33e3adb99e1c&j=70066679-cdfb-41af-b41f-345be6fcc973&j=d92de444-9fcb-4145-8239-7837835b21f9&j=4d955e47-631b-4092-8f24-277d6669b270&j=6b9e2415-633e-4e81-bb33-ac46f9b76de2&j=f10aa772-badc-4448-90af-afbdad430042&j=3ecac374-73db-4b5b-a850-b2387eb9d5c4&j=5081356f-27c5-437b-aa08-733299b952e2&j=b81a2d7b-2029-4820-ba89-c0f97da53c5a&j=6a373f92-6d67-4c3a-92a3-8b31425547fb&j=379c2abc-c6d9-490b-9f96-efc9e6659c0e&j=2077a337-e6b1-4a52-942d-fdb907418dce&j=ee39d96e-961a-47e8-98b9-6d6a09d24cea&m=07f4fee0bdd55252ba3e372a4d20a5cc&m=d0e91d56aaa75472b86b427775948b86&m=d51b74499a275579ae0f34b98758f123&m=94f285525dd055a7a6e6da7fcdfbfa6d&m=f66581cf148454b9aa126506cc0078b1&m=05d2a6dea83b56c2a9af78266ff2e552&m=98de385ebff956f6af00628cdd6eb8e4&m=2f91ea06514b545aa8c693e03c076660&m=a13c183793b25f67a3e08ee9de26d4ed&m=603102f09e3f5ad99538175719970bde&m=14a1d71df21558e5ade0214f90482cdc&m=24295ca1259a5876ba7bf8ef496feed6&m=383f18001b395f39825061a5c0798fad&m=018d01410efb5472a6989328817df00a&m=941c2e759f325408a946031217b6d669&page={}&toDate={}T00%3A00%3A00"
    all_data = pd.DataFrame()
    
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        page_number = 0
        while True:
            url = base_url.format(StartDate,page_number,EndDate)
            html = get_html_with_selenium(url, driver)
            selector = Selector(text=html)
            infos = get_info(selector)
            if not infos:
                break
            df = pd.DataFrame(infos)
            all_data = pd.concat([all_data, df], ignore_index=True)
            page_number += 1
            next  = selector.xpath("/html/body/div/div/div/div[2]/div/div[2]/div[2]/nav/ul/li[4]/button/@aria-disabled").get()
            print(next.strip())
            if next.strip() == "true":
                break
        print(page_number)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return all_data

if __name__ == "__main__":
    StartDate,EndDate = "2024-08-06","2024-08-06"
    df = statstidende(StartDate,EndDate)
    save_to_excel(df, 'statstidende_data.xlsx')
 