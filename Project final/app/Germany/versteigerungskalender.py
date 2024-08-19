import requests
from scrapy import Selector
#from tools import save_to_excel
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from tools import save_to_excel,translate_to_en,convert_to_df


# Function to get page source using requests
def get_html(url):
    response = requests.get(url)
    return response.text

# Function to extract information from the HTML using XPath
def get_info(selector):
    items = selector.xpath(".//*[@id='results']/ul/li[@class='transition-all duration-300 border-b even:bg-alpha-50 even:hover:bg-alpha-100 odd:bg-white odd:hover:bg-alpha-100 border-alpha-200']")
    
    all_info = []
    for item in items:
        title = item.xpath(".//a/p[@class='col-span-4 text-balance']/text()").get().strip()
        category = item.xpath(".//a/p[2]/span/text()").extract()
        category = clean_data(category)
        location = item.xpath(".//a/p[@class='col-span-4']/text()").get().strip()
        link = item.xpath(".//a/@href").get()

        # Scraping additional data from the detail page
        date, company_id = get_date_and_id(link)
        info = {
            "ID": company_id,
            "Title": title,
            "Date": date,
            "Location": location,
            "Category": category,
            "Link": link
        }
        all_info.append(info)
    
    return all_info



def clean_data(data):
    cleaned_data = [item.strip() for item in data]
    return ' '.join(cleaned_data)

# Function to get date and ID from detail page
def get_date_and_id(detail_url):
    html = get_html(detail_url)
    selector = Selector(text=html)
    date = selector.xpath("/html/body[@class='font-sans-serif text-base w-full antialiased text-black leading-relaxed flex flex-col min-h-screen ']/main[@class='flex-1 pb-20']/div[@class='content-wrapper']/div[@class='md:grid md:grid-cols-[1fr_minmax(20rem,_25%)] md:gap-x-4 mt-8']/div[1]/div[@class='grid grid-cols-1 mt-12 gap-x-4 lg:grid-cols-2']/div[@class='py-8 border-t border-b border-alpha-200']/p/text()").get()
    date = date.strip().replace("Veröffentlicht: ", "") if date else "N/A"
    company_id = selector.xpath("/html/body/main/div/div[1]/div[1]/div[1]/div[2]/div/button/span/text()").get()
    company_id = company_id.strip() if company_id else "N/A"
    return date, company_id

def next_page(selector):
    next_button = selector.xpath("/html/body/main/section/div/div[2]/div[2]/div/nav/a[5]/span/text()").get()
    return next_button == "Next"

def next_page2(selector):
    next_button = selector.xpath("/html/body/main/section/div/div[2]/div[2]/div/nav/a[6]/span/text()").get()
    return next_button == "Next"

# Main function to scrape the auction site
def verstei(keywords, sector="40112"):
    base_url = "https://www.versteigerungskalender.de/insolvenzkalender?search={}&location=&radius=&brSector={}&orderBy=title&sortBy=asc&page={}"
    page = 1
    all_data = pd.DataFrame()

    with ThreadPoolExecutor() as executor:
        futures = []
        while True:
            url = base_url.format(keywords, sector, page)
            html = get_html(url)
            selector = Selector(text=html)
            infos = get_info(selector)
            df = convert_to_df(infos)
            all_data = pd.concat([all_data, df], ignore_index=True)

            if next_page(selector) or next_page2(selector):
                page += 1
                print("\n",page,"\n")
            else:
                break
    return all_data


# Test
if __name__ == "__main__":
    keywords = "v"
    
    data = verstei(keywords)
    save_to_excel(data, "verstei_data.xlsx")
