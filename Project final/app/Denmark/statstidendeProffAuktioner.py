# This code is for scraping the statstidendeProffAuktioner site (Denmark court site)
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from scrapy import Selector
from tools import convert_to_df, translate_to_en, save_to_excel,isInSelligent
try:
    from .proff import proff
    from .auktioner import auktioner
    from .StatstidendeMessages import statstidendemessages
    from .opencorporates import opencorporates
except:
    from proff import proff
    from auktioner import auktioner
    from StatstidendeMessages import statstidendemessages
    from opencorporates import opencorporates

from datetime import datetime

# Function to get page source using Selenium
def get_html_with_selenium(url, driver):
    driver.get(url)
    sleep(5)  # Give time for the page to fully load (adjust as needed)
    html = driver.page_source
    return html

# Function to extract information from the HTML using XPath
def get_info(selector,selligent,trans):
    items = selector.xpath("//div[@class='message-entry py-3 pl-sm-0 container']")
    
    all_info = []
    for item in items:
        title = item.xpath(".//div[@class='message-number']/text()").get()
        company_name = item.xpath(".//a/h3[@class='pt-2 pt-sm-0']/text()").get()
        num_cvr = item.xpath(".//div[@class='message-summary'][1]/div/text()").get()
        court_district = item.xpath(".//div[@class='message-summary'][1]/div[2]/text()").get()
        date_annonce = item.xpath(".//div[@class='message-summary'][2]/div[@class='message-date']/text()").get()
        
        if "CVR-nr.:" in num_cvr and selligent and isInSelligent(num_cvr.replace("CVR-nr.: ", "").strip())==False:
            
            address,domaine,status = proff(num_cvr.replace("CVR-nr.: ", "").strip())
            try:
                Curator,Decree,Official = auktioner(num_cvr.replace("CVR-nr.: ", "").strip())
            except:
                Curator=''
            
            Curator=" | ".join(Curator)

            if Curator=='':
                try:
                    Rapport,Curator = statstidendemessages(num_cvr.replace("CVR-nr.: ", "").strip())
                except:
                    Curator='404'
            if status==''or domaine==''or address=='':
                try:
                    list= opencorporates(num_cvr.replace("CVR-nr.: ", "").strip())
                    status = list['Status']
                    print(status)
                    address = list['Registered Address']
                    print(address)
                    domaine = list['Industry Codes']
                    print(domaine)
                except:
                    status = '404'
                    domaine = '404'
                    address='404'






        else:
            if "CVR-nr.:" in num_cvr:
                address,domaine,status = proff(num_cvr.replace("CVR-nr.: ", "").strip())
                try:
                    Curator,Decree,Official = auktioner(num_cvr.replace("CVR-nr.: ", "").strip())
                except:
                    Curator=''
            
                Curator=" | ".join(Curator)

                if Curator=='':
                    try:
                        Rapport,Curator = statstidendemessages(num_cvr.replace("CVR-nr.: ", "").strip())
                    except:
                        Curator='404'
                if status==''or domaine==''or address=='':
                    try:
                        list= opencorporates(num_cvr.replace("CVR-nr.: ", "").strip())
                        status = list['Status']
                        print(status)
                        address = list['Registered Address']
                        print(address)
                        domaine = list['Industry Codes']
                        print(domaine)
                    except:
                        status = '404'
                        domaine = '404'
                        address='404'


                
        if "CVR-nr.:" in num_cvr: 
            if trans:
                info = {
            "Decree date(auktioner)": Decree if Decree else '', 	   	
            "Official Gazette date(auktioner)": Official if Official else '',
            "Court Message": translate_to_en(title.strip() if title else ''),
            "Company Name": company_name.strip() if company_name else '',
            "N° CVR": num_cvr.replace("CVR-nr.: ", "").strip() if num_cvr else '',
            "Court District": court_district.replace("Retskreds: ", "").strip() if court_district else '',
            "Date Annonce (statstidende)": date_annonce.replace("Kundgørelsesdato: ", "").strip() if date_annonce else '',
            "Address":address.strip() if address else '',
            "Domaine":translate_to_en(domaine.strip() if domaine else ''),
            "Status":translate_to_en(status.strip() if status else '') ,
            "Curator": Curator if Curator else '',
            
            

            }
            else:
                info = {
            "Decree date(auktioner)": Decree if Decree else '', 	   	
            "Official Gazette date(auktioner)": Official if Official else '',
            "Court Message": title.strip() if title else '',
            "Company Name": company_name.strip() if company_name else '',
            "N° CVR": num_cvr.replace("CVR-nr.: ", "").strip() if num_cvr else '',
            "Court District": court_district.replace("Retskreds: ", "").strip() if court_district else '',
            "Date Annonce (statstidende)": date_annonce.replace("Kundgørelsesdato: ", "").strip() if date_annonce else '',
            "Address":address.strip() if address else '',
            "Domaine":domaine.strip() if domaine else '',
            "Status":status.strip() if status else '' ,
            "Curator": Curator if Curator else '',
                }
            all_info.append(info)
            print(info)
        
    
    return all_info
# Main function to perform the scraping and saving
def statstidendeProffAuktioner(StartDate,EndDate,selligent=False,trans=True):
    base_url = "https://www.statstidende.dk/messages?fromDate={}T00%3A00%3A00&page={}&ps=100&toDate={}"
    print(StartDate)
    print(EndDate)
    all_data = pd.DataFrame()
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    page_number = 0
    while True:

        url = base_url.format(StartDate,page_number,EndDate)
        html = get_html_with_selenium(url, driver)
        selector = Selector(text=html)
        infos = get_info(selector,selligent,trans)
        df = pd.DataFrame(infos)
        all_data = pd.concat([all_data, df], ignore_index=True)
        page_number += 1
        next  = selector.xpath('//button[@id="Næste"]/@class').get()
        print(next)
        print(type(next))
        if "disabled" in next:
            break
        
        
    driver.close()
    
    return all_data

if __name__ == "__main__":
    start_time = datetime.now()
    StartDate,EndDate = "2024-08-15","2024-08-15"
    df = statstidendeProffAuktioner(StartDate,EndDate,selligent=False,trans=True)
    end_time = datetime.now()
    duration = end_time - start_time
    print(duration)
    save_to_excel(df, 'statstidendeProffAuktioner_Duration.xlsx')
    