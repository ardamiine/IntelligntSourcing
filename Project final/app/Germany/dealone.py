import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from scrapy import Selector
from tools import convert_to_df, translate_to_en


# Function to initialize Selenium webdriver and login
def initialize_driver_and_login(username, password):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    
    # Login to the website
    login_url = "https://www.deal-one.de/wp-login.php"
    driver.get(login_url)
    sleep(5)  # Ensure page is loaded

    # Fill in login details
    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)
    driver.find_element(By.ID, "wp-submit").click()
    sleep(5)  # Wait for login to complete

    return driver

# Function to get page source using Selenium
def get_html_with_selenium(url, driver):
    driver.get(url)
    sleep(5)  # Give time for the page to fully load (adjust as needed)
    html = driver.page_source
    return html

# Function to extract information from the HTML using XPath
def get_info(selector):
    items = selector.xpath("//div[@class='item-listing-wrap hz-item-gallery-js card']")

    all_info = []
    for item in items:
        title = item.xpath(".//h2[@class='item-title']/a/text()").get()
        region = item.xpath(".//div[@class='card-table-row'][1]/span[2]/text()").get()
        category = item.xpath(".//div[@class='card-table-row'][2]/span[2]/text()").get()

        revenue = item.xpath(".//div[@class='card-table-row'][3]/span[2]/text()").get()
        employees = item.xpath(".//div[@class='card-table-row'][4]/span[2]/text()").get()
        ebit = item.xpath(".//div[@class='card-table-row'][5]/span[2]/text()").get()
        link = item.xpath(".//h2[@class='item-title']/a/@href").get()

        info = {
            "Title": title.strip() if title else '',
            "Region": region.strip() if region else '',
            "Category": translate_to_en(category.strip()) if category else '',
            "Revenue": revenue.strip() if revenue else '',
            "Employees": employees.strip() if employees else '',
            "EBIT": ebit.strip() if ebit else '',
            "Link": link if link else ''
        }
        all_info.append(info)

    return all_info

# Function to save DataFrame to Excel
def save_to_excel(df, base_filename):
    directory = "download"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(directory, f"{os.path.splitext(base_filename)[0]}_{counter}.xlsx")
        counter += 1

    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")
    
    return filename

# Main function to perform the scraping and saving
def deal(keywords, username="5c61886147@emailcbox.pro", password="Xzabam12"):
    base_url = "https://www.deal-one.de/suchergebnisse/page/{}/?keyword={}"
    all_data = pd.DataFrame()

    # Initialize Selenium webdriver and login
    driver = initialize_driver_and_login(username, password)

    try:
        page_number = 1
        while True:
            url = base_url.format(page_number, keywords)
            html = get_html_with_selenium(url, driver)
            selector = Selector(text=html)
            infos = get_info(selector)
            if not infos:
                break
            df = convert_to_df(infos)
            all_data = pd.concat([all_data, df], ignore_index=True)
            page_number += 1
            print(page_number)
    finally:
        driver.quit()  # Ensure webdriver is closed even if an exception occurs

    return all_data

if __name__ == "__main__":
    keywords = "hhhhhh"
    username = "5c61886147@emailcbox.pro"
    password = "Xzabam12"
    data = deal(keywords, username, password)
    save_to_excel(data, "deal-one_data.xlsx")
