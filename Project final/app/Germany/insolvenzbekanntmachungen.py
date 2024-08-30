from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tools import analyse_rapport,save_to_excel,convert_to_df,translate_to_en,isInSelligent

def get_dates_between(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    dates_between = []
    current_date = start_date
    while current_date <= end_date:
        dates_between.append(current_date.strftime("%d-%m-%Y"))
        current_date += timedelta(days=1)
    return dates_between

def converttoHtml(url,datem,dateM,mot):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-search-engine-choice-screen')
    dr=webdriver.Chrome(options=chrome_options)
    dr.get(url)
    element = dr.find_element(by='id', value="frm_suche:ldi_datumVon:datumHtml5")
    element.clear()  # Optional: Use this if you want to clear the existing value first
    element.send_keys(datem)
    element = dr.find_element(by='id', value="frm_suche:ldi_datumBis:datumHtml5")
    element.clear()  # Optional: Use this if you want to clear the existing value first
    element.send_keys(dateM)
    element = dr.find_element(by='id', value="frm_suche:litx_firmaNachName:text")
    element.send_keys(mot+Keys.ENTER)
    time.sleep(1)
    html=dr.page_source
    h=[]
    time.sleep(0.5)
    try:
        elements=dr.find_elements(by="xpath",value='.//input[@title="Veröffentlichungstext anzeigen"]')
        for element in elements:
            main_window = dr.current_window_handle
            dr.execute_script("arguments[0].click();",element)
            window_handles = dr.window_handles
            for handle in window_handles:
                if handle != main_window:
                    dr.switch_to.window(handle)
                    break
            time.sleep(0.25)
            elemen=dr.find_element(by="xpath",value=".//body")
            h.append(elemen.text)
            dr.close()
            dr.switch_to.window(main_window)
    except:
        pass
    dr.close()
    return html,h

def is_valid_date(date_str, format='%d.%m.%Y'):
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def FindBt(t):
    for i in range(len(t)):
        if is_valid_date(t[i]):
            return i
    return -1

def SplitList(info):
    u=[]
    while True:
        x=FindBt(info)
        if (FindBt(info[x+1:])!=-1):
            x=FindBt(info[x+1:])
            u.append(info[:x+1])
            info=info[x+1:]
        else:
            u.append(info)
            break
    return u

def get_alldata(i,datem,dateM):
    url="https://neu.insolvenzbekanntmachungen.de/ap/ergebnis.jsf"
    html,d=converttoHtml(url,datem,dateM,i)
    d=pd.DataFrame({"Rapport":d})
    alldata=pd.DataFrame()
    S=Selector(text=html)
    columns=['Release date','current file number','Court','Name, first name / designation','Registered office / residence','Register']
    h=S.xpath(".//table[@id='tbl_ergebnis']/tbody//tr//td//text()").extract()
    print("\n H",h,"\n")
    h=[a for a in h if a!="\n"]
    if len(h)>0:
        h = SplitList(h)
    df=pd.DataFrame(h,columns=columns)
    df=df.join(d)
    df=df[df["current file number"].str.contains("/24|/23")]
    alldata=pd.concat([alldata,df],ignore_index=True)
    return alldata

def Acceptall(d):
    d.execute_script("""
    document.querySelector("#usercentrics-root").shadowRoot.querySelector("#uc-center-container > div.sc-eBMEME.dRvQzh > div > div.sc-jsJBEP.iXSECa > div > button:nth-child(3)").click();
    """)

def ListToString(x):
    return " ".join(x).strip(", ")

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
    btn=driver.find_element(by="xpath",value="html/body/div[1]/div/div/div/div[2]/div/div[2]/form/button")
    driver.execute_script("arguments[0].click();",btn)
    time.sleep(3)

def get_data(i):
    url1="https://www.creditreform.de/suche"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_extension(r"C:\Users\amine.ardhaoui\Desktop\Intellegent sourcing V1\Project final\app\Germany\buster.crx")
    dr=webdriver.Chrome(options=options)
    dr.get(url1)
    time.sleep(2)
    try:
        Acceptall(dr)
    except:
        pass
    try:
        element = dr.find_element(by="xpath",value='//*[@id="tx-solr-search-form-pi-results"]/div/input')
        element.send_keys(i+Keys.ENTER)
    except:
        pass
    time.sleep(2)

    try:

        element = dr.find_element(by="xpath",value='//*[@id="tx-solr-search"]/div[3]/div/div[2]/div/div/div[2]/a[1]')
        dr.execute_script("arguments[0].click();",element)
        k=1
    except:
        k=0

    time.sleep(2)
    if k==1:
        all_handles = dr.window_handles
        dr.close()
        dr.switch_to.window(all_handles[1])
        link=dr.current_url
        time.sleep(3)
        if "captcha" in dr.current_url.lower():
            captcha(dr)
        try:

            element = dr.find_element(by="xpath",value="html/body/div[1]/div/div[4]/div[1]/div[4]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div[2]/p/span")
            dr.execute_script("arguments[0].click();",element)
        except:
            try:

                element = dr.find_element(by="xpath",value="/html/body/div[1]/div/div[4]/div[1]/div[4]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/p/span")
                dr.execute_script("arguments[0].click();",element)
            except:
                pass

        time.sleep(1)
        html=dr.page_source
        dr.close()
        return [html,link]
    else:
        dr.close()
        return ["None","None"]

def AppendDataFrames(alldata,d):
    df=pd.DataFrame(d)
    df["Namecompany"] = df["Name"].apply(lambda x: x.split(", ")[0] if ", " in x else x)
    df["Region"]=df["Name"].apply(lambda x: x[x.find(", ")+2:].strip())
    df=df[["URL","Teliphone","Email","WebSite","Purpose","Namecompany","Region"]]
    all_data=alldata.merge(df,left_on=["Name, first name / designation","Registered office / residence"],right_on=["Namecompany","Region"])
    all_data.drop(columns=["Namecompany","Region"],inplace=True)
    return all_data

def Insolvenzbekanntmachungen(keyword,datem,dateM,selligent=False,trans=True):
    ad = get_alldata(keyword, datem, dateM)

    if len(ad) == 0:
        dates = get_dates_between(datem, dateM)
        for j in dates:
            d = get_alldata(keyword, j, j)
            ad = pd.concat([ad, d])
    if selligent==True:
        df=ad
        df['selligent_result'] = df['Name, first name / designation'].apply(isInSelligent)
        filtered_df = df[df['selligent_result'] == False]
        # Drop the helper column if needed
        ad = filtered_df.drop(columns='selligent_result')
    # Add a new column 'Status' initialized to 0 for every rapport
    ad['Status'] = "" 

    # Analyze each rapport and update the Status
    for index, row in ad.iterrows():
        rapport_analysis = analyse_rapport(row['Rapport'])
        ad.at[index, 'Status'] = rapport_analysis

    l=ad["Name, first name / designation"]+", "+ad["Registered office / residence"]
    l=l.to_list()
    l=list(set(l))
    d=[]
    k=0
    for i in range(len(l)):
        k+=1
        print(f"{k}/{len(l)}")
        t=get_data(l[i])
        html=t[0]
        link=t[1]
        if html!="None":
            S=Selector(text=html)
            email=ListToString(S.xpath(".//p[@class='adres-white cursor-pointer']//text()").extract())
            tel=ListToString(S.xpath('.//p[@class="adres-white"]//span//text()').extract())
            site=ListToString(S.xpath('.//a[@class="text-white cursor-pointer"]//text()').extract())
            propose=ListToString(S.xpath("//*[@id='firmenauskunft']/div/p/span/text()").extract())
            dic={
                "Name":l[i],
                "URL":link,
                "Teliphone":tel,
                "Email":email,
                "WebSite":site,
                "Purpose":translate_to_en(propose) if trans==True else propose
            }
        else:
            dic={
                "Name":l[i],
                "URL":"None",
                "Teliphone":"",
                "Email":"",
                "WebSite":"",
                "Purpose":""
            }
        d.append(dic)
    return AppendDataFrames(ad,d)

#Testing


if __name__ == "__main__":
    keyword="*GMbH" 
    datem="11-08-2024"
    dateM="11-08-2024"
    data = Insolvenzbekanntmachungen(keyword,datem,dateM,selligent=False,trans=True)
    print(data)

    save_to_excel(data,"insolv.xlsx")
    