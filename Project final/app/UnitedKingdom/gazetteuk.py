from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime
import pandas as pd
import requests
from tools import save_to_excel
from math import ceil
 
from .endole import endole
 
import json
 
 
def get_day_of_date(date_str,mot):
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    if mot=="y":
        return date_obj.year
    elif mot=="d":
        return date_obj.day
    else:
        return date_obj.month
 
def converToHtml(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    dr=webdriver.Chrome(options=chrome_options)
    dr.get(url)
    html=dr.page_source
    dr.close()
    return html
 
def get_numberOf_pages(url):
    s=Selector(text=converToHtml(url))
    try:
        a=int(s.xpath(".//header//p[@class='number-notices']//text()").extract()[0].split(" ")[-2])/100
    except:
        a=0
    return ceil(a)
 
def GetLinks(s):
    links=s.xpath(".//h3[@class='title']/a/@href").extract()
    pattern = r'/notice/\d+'
    links = [url for url in links if re.match(pattern, url)]
    return ["https://www.thegazette.co.uk"+i for i in links]
 
def GetCode(s):
    c=s.xpath(".//div[@class='notice-summary']//a/@href").extract()
    pattern = r'/company/\d+'
    return [i for i in c if re.match(pattern, i)]
 
def GetStatus(s):
    a=s.xpath(".//article/div/dl[2]/dd/text()").extract()
    return [i.strip() for i in a]
 
def FilterList(o,indexs):
    if len(o)==0:
        return []
    return [o[i] for i in indexs]
 
def GetIndex(t):
    #return [i for i,j in enumerate(t) if ((j not in["Amendment of Title of Proceedings","Qualifying Decision Procedure","Notice of Intended Dividend","Notice of Dividends","Notice of Intended Dividends","Notice of Intended Dividends","Bankruptcy Orders"])and "Dismissal" not in j)]
    return [i for i,j in enumerate(t) if ("LTD" in j)or("LIMITED" in j)or("PLC" in j)]
 
def GetCompanyNames(s):
    a=s.xpath(".//h3[@class='title']/a/text()").extract()
    return [i.strip() for i in a if (i not in['The Gazette','Policies','clear all'])]
 
def GetAdress(s):
    a=s.xpath(".//p[@data-gazettes='CompanyRegisteredOffice']//span//text() | .//span[@about='this:company-1-address-0']//text() | .//span[@about='this:company-registered-office-1']//text()").extract()
    #b=s.xpath(".//span[@about='this:company-registered-office-1']//text()").extract()
    #d=s.xpath(".//span[@about='this:company-1-address-0']//text()")
    if len(a)>0:
        c=",".join(a).strip().replace("The registered office of the Company will be changed to 4th Floor, Fountain Precinct","").strip()
        c=' '.join(c.split(", "))
        return c
    else:
        return ""
 
def correctName(f,m,l):
    if (len(f)==len(l)==len(m)):
        return [f[i]+" "+m[i]+" "+l[i] for i in range(len(f))]
    elif (len(f)==len(l)):
        return [f[i]+" "+l[i] for i in range(len(f))]
    elif (len(f)==0)and(len(l)>0):
        return l
    elif (len(l)==0)and(len(f)>0):
        return f
    else:
        return ""
 
def GetResponsibleName(s):
    forname=s.xpath(".//span[@data-gazettes='Forename']//text()").extract()
    surname=s.xpath(".//span[@data-gazettes='Surname']//text()").extract()
    midlename=s.xpath(".//span[@data-gazettes='MiddleNames']//text()").extract()
    fullname=correctName(forname,midlename,surname)
    fullname2=s.xpath('.//span[@property="foaf:name"]/text()').extract()
    if len(fullname2)>0:
        return ",".join(fullname2).strip()
    elif len(fullname)>0:
        return ",".join(fullname).strip()
    else:
        return ""
 
def GetTel(text):
    phone_pattern = re.compile(r'''
    (\+44\s?\d{3,4}\s?\d{3}\s?\d{3,4}) |  # +44 international format
    (\b\d{5}\s?\d{6}\b) |                 # 5+6 digit format (e.g., 01202 237337)
    (\b\d{4}\s?\d{3}\s?\d{3,4}\b) |       # 4+3+3 or 4+3+4 digit format
    (\b\d{2,3}\s?\d{4}\s?\d{4}\b) |       # 2+4+4 or 3+4+4 digit format (e.g., 020 8446 6699)
    (\b\d{11}\b) |                        # 11 digit format without spaces (e.g., 03330050080)
    (\b\d{5}\s?\d{3}\s?\d{3}\b)           # 5+3+3 digit format (e.g., 02380 221 222)
    ''', re.VERBOSE)
 
    # Find all matches in the text
    matches = phone_pattern.findall(text)
 
    # Flatten the list of tuples and filter out empty strings
    return ",".join([number for match in matches for number in match if number])
 
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return ",".join(emails)
 
def uk(datemin,datemax):
    url=f"https://www.thegazette.co.uk/insolvency/notice?text=&insolvency_corporate=G205010000&insolvency_personal=G206030000&location-postcode-1=&location-distance-1=1&location-local-authority-1=&numberOfLocationSearches=1&start-publish-date={get_day_of_date(datemin,'d')}%2F{get_day_of_date(datemin,'m')}%2F{get_day_of_date(datemin,'y')}&end-publish-date={get_day_of_date(datemax,'d')}%2F{get_day_of_date(datemax,'m')}%2F{get_day_of_date(datemax,'y')}&edition=&london-issue=&edinburgh-issue=&belfast-issue=&sort-by=&results-page-size=100"
    pages=get_numberOf_pages(url)
    print(pages)
    AllData=[]
    for j in range(1,pages+1):
            url2=url+"&results-page="+str(j)
            S=Selector(text=converToHtml(url2))
            companynames=GetCompanyNames(S)
            index=GetIndex(companynames)
            companynames=FilterList(companynames,index)
            status=FilterList(GetStatus(S),index)
            #index=GetIndex(status)
            links=FilterList(GetLinks(S),index)
            dates=FilterList(S.xpath(".//time//text()").extract(),index)
            if (len(links)>0):
                for i,link in enumerate(links):
                    S=Selector(text=converToHtml(link))
                    code=GetCode(S)
                    if len(code)>0:
                        pattern = r'/company/\d+'
                        code = [url for url in code if re.match(pattern, url)][0]
                        code=code.replace("/company/","")
                        adress=GetAdress(S)
                        resp=GetResponsibleName(S)
                        article=S.xpath(".//div[contains(@class,'full-notice full-notice-')]//div[@class='content']//text()").extract()
                        email=[i for i in extract_emails("".join(article)).split(",") if i != "customer.services@thegazette.co.uk"]
                        email=",".join(email)
                        tel=",".join(list(set(GetTel("".join(article)).split(','))))
                        cn=S.xpath(".//*[@data-gazettes='NatureOfBusiness']//span//text()").extract_first()
                        try:
                            statuss,CreationDate,totalAssets,contact = endole(code)
                            contact = json.loads(contact)
                            RegisteredAddress = contact.get("Registered Address")
                            Website = contact.get("Website")
                           
                        except:
                            statuss,CreationDate,totalAssets,RegisteredAddress,Website='','','','',''
 
                       
                        dic={"Date":dates[i],
                            "Company Name":companynames[i],
                            "Company Code":code,
                            "Company Status":status[i],
                            "Nature of Business":cn,
                            "Adress":adress ,
                            "Registered Address":RegisteredAddress if RegisteredAddress else '',
                            "UrlLink":link,
                            "Responsible Name":resp,
                            "Responsible Email":email,
                            "Responsible PhoneNumber":tel,
                            "Website":Website if Website else'',
                            "Total Assets":totalAssets,
 
                            }
           
                        AllData.append(dic)
                        print(dic)
           
            print("\n \npage:",j)
    return AllData
 
def GazetteUK(datemin,datemax):
    all=uk(datemin,datemax)
    df=pd.DataFrame(all)
    print(df.columns)
    l=["SERVICES","RESTAURANT","Logistics", "ASSOCIATION","HOLDINGS","CATERING","FORBISHMENT","BUILDING"]
    pattern = '|'.join(l)
    excel=df[~df["Company Name"].str.contains(pattern)]
    excel = excel.drop_duplicates(subset=["Date", "Company Name", "Company Code"], keep="last")
    return excel
 
if __name__=="__main__":
    start_time = datetime.now()
    df=GazetteUK("15-08-2024","15-08-2024")
    end_time = datetime.now()
    duration = end_time - start_time
    print(duration)
    save_to_excel(df,"guazette_data.xlsx")