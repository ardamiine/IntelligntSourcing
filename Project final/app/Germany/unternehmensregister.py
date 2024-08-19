from selenium import webdriver
import time
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import date
from tools import save_to_excel

def getHtmls(StartDate,EndDate):
    url="https://www.unternehmensregister.de/ureg/search1.7.html;jsessionid=0E375841C17D08BADA339E86841660E9.web01-1"
    options=Options()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    dr=webdriver.Chrome(options=options)
    dr.get(url)
    element=dr.find_element(by="id",value="cc_all")
    element.click()
    element=dr.find_element(by="id",value="select2-searchInsolvencyFormbankruptciesRegisterLocation-container")
    element.click()
    element=dr.find_element(by="css selector",value=".select2-search__field")
    element.send_keys("Aachen"+Keys.ENTER)
    element=dr.find_element(by="id",value="select2-searchInsolvencyFormbankruptciesRegisterType-container")
    element.click()
    element=dr.find_element(by="xpath",value=".//li[text()='HRB']")
    element.click()
    element=dr.find_element(by="id",value="select2-searchInsolvencyFormbankruptciesCourtId-container")
    element.click()
    element=dr.find_element(by="css selector",value=".select2-search__field")
    element.send_keys("Aachen"+Keys.ENTER)
    element=dr.find_element(by="id",value="searchInsolvencyForm:bankruptciesCourtName")
    element.send_keys("Aachen")
    element=dr.find_element(by="id",value="select2-searchInsolvencyFormbankruptciesPublicationType-container")
    element.click()
    element=dr.find_element(by="css selector",value=".select2-search__field")
    element.send_keys("Eroffnungen"+Keys.ENTER)
    element=dr.find_element(by="id",value="searchInsolvencyForm:bankruptciesPublicationsStartDate")
    element.send_keys(StartDate)
    element=dr.find_element(by="id",value="searchInsolvencyForm:bankruptciesPublicationsEndDate")
    element.send_keys(EndDate+Keys.ENTER)
    time.sleep(2)
    elements=dr.find_elements(by="css selector",value=".page_count")
    numpages=elements[0].text
    numpages=int(numpages[:numpages.find("Seiten")].strip())
    htmls=[]
    htmls.append(dr.page_source)
    if numpages>1:
        for i in range(numpages-1):
            element=dr.find_element(by="xpath",value=".//*[@id='content']/section[2]/div/div/div/div/div[5]/div[2]/nav/div/div[3]/div[1]/a")
            element.click()
            time.sleep(2)
            htmls.append(dr.page_source)
    dr.close()
    return htmls

def get_Code(text):
    pattern = r"\b\d+ IN \d+/\d+\b"
    return re.search(pattern, text).group(0)

def get_year():
    today = date.today()
    current_year = today.year
    return current_year-2000

def get_DataFrame(StartDate,EndDate):
    d=[]
    htmls=getHtmls(StartDate,EndDate)
    for i in htmls:
        S=Selector(text=i)
        names=S.xpath(".//div[@class='row']//div[@class='company_result']//span/text()").extract()
        code=S.xpath(".//div[@class='row']//div[@class='company_result']//text()").extract()
        code=[i.strip() for i in code if (len(i.strip())>0)and(" IN " in i.strip())]
        for i in range(len(code)):
            dic={
                "CompanyName":names[i],
                "CompanyCode":code[i]
            }
            d.append(dic)
    df=pd.DataFrame(d)
    y=get_year()
    df["CompanyCode"]=df["CompanyCode"].apply(get_Code)
    df=df[df["CompanyCode"].str.contains("/"+str(y)+"|/"+str(y-1)+"")].reset_index( drop=True)
    return df

def ListToString(x):
    return " ".join(x).strip(", ")

def Acceptall(d):
    click_coordinates = {'x': 724, 'y': 438}
    action = ActionChains(d)
    action.move_by_offset(click_coordinates['x'], click_coordinates['y']).click().perform()

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
    time.sleep(1)
    btn=driver.find_element(by="xpath",value="html/body/div[1]/div/div/div/div[2]/div/div[2]/form/button")
    driver.execute_script("arguments[0].click();",btn)
    time.sleep(2)

def get_data(i):
    url1="https://www.creditreform.de/suche"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options = webdriver.ChromeOptions()
    options = Options()
    #options.add_argument("--headless")
    options.add_extension(r"app\buster.crx")
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

def unternehmensregister(StartDate,EndDate):
    df=get_DataFrame(StartDate,EndDate)
    print(df)
    l=df["CompanyName"]
    l=l.to_list()
    l=list(set(l))
    d=[]
    for i in l:
        t=get_data(i)
        html=t[0]
        link=t[1]
        if html!="None":
            S=Selector(text=html)
            email=ListToString(S.xpath(".//p[@class='adres-white cursor-pointer']//text()").extract())
            tel=ListToString(S.xpath('.//p[@class="adres-white"]//span//text()').extract())
            site=ListToString(S.xpath('.//a[@class="text-white cursor-pointer"]//text()').extract())
            propose=ListToString(S.xpath("//*[@id='firmenauskunft']/div/p/span/text()").extract())
            dic={
                "Name":i,
                "URL":link,
                "Teliphone":tel,
                "Email":email,
                "WebSite":site,
                "Purpose":propose
            }
        else:
            dic={
                "Name":i,
                "URL":"None",
                "Teliphone":"",
                "Email":"",
                "WebSite":"",
                "Purpose":""
            }
        d.append(dic)
        print(d)
    df2=pd.DataFrame(d)
    df2=df2.merge(df,left_on="Name",right_on="CompanyName")
    df2=df2[["Name","CompanyCode","URL","Teliphone","Email","WebSite","Purpose"]]
    return df2


if __name__ == "__main__":
    StartDate = "01-07-2024"
    EndDate = "05-07-2024"
    data = unternehmensregister(StartDate,EndDate)
    save_to_excel(data,"test.xlsx")