from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

def proff(i):
    options=Options()
    options.add_argument("--headless")
    driver=webdriver.Chrome(options=options)
    driver.get(f"https://www.proff.dk/branches%C3%B8g?q={i}")
    try:
        element=driver.find_element(by="xpath",value="//*[@id='qc-cmp2-ui']/div[2]/div/button[3]/span")
        element.click()
    except:
        pass
    elements = driver.find_elements(by="xpath", value=".//a[@class='MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover addax addax-cs_hl_hit_company_name_click mui-105wgyd']")
    try:
        if len(elements)>2:
            elements[1].click()
        else:
            elements[0].click()
    except:
        pass
    address,domaine,status=["","",""]
    sleep(1)
    try:
        element = driver.find_element(by="xpath", value=".//div[@class='MuiBox-root mui-ifq4c4']//span[@class='MuiTypography-root MuiTypography-body2 companyId-address mui-bttkri']")
        address = element.text
    except:
        pass

    try:
        element = driver.find_element(by="xpath", value=".//div[@class='MuiGrid-root MuiGrid-container MuiGrid-item mui-1orsd3g']//p[@class='MuiTypography-root MuiTypography-body2 mui-bttkri']")
        domaine = element.text
    except:
        pass

    try:
        element = driver.find_element(by="xpath", value=".//div[@class='MuiBox-root mui-0']//span[@class='MuiTypography-root MuiTypography-body2 mui-85se3v']")
        status = element.text
    except:
        pass
    driver.close()
    return address,domaine,status

if __name__=="__main__":
    proff("39158043")