import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

searchterm = 'sony a7 iii'

def get_data(searchterm, page):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&_pgn={page}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    if not results:
        return None
    
    for item in results:
        price_text = item.find('span', {'class': 's-item__price'}).text
        clean_price = re.findall(r'\d+\.\d+', price_text)  # Find all price-like patterns (e.g., 107.99)
        
        # If multiple prices are found, take the first one
        soldprice = float(clean_price[0]) if clean_price else 0.0
        product = {
            'title': item.find('div', {'class': 's-item__title'}).find('span', {'role': 'heading'}).text,
            'link' : item.find('a', {'class': 's-item__link'})['href'],
            'soldprice': soldprice,
            'bids': item.find('span', {'class': 's-item__bids'}).text if item.find('span', {'class': 's-item__bids'}) else 'N/A'
            
        }
        productslist.append(product)
    return productslist


def output(productlist, shearchterm):
    productsdf = pd.DataFrame(productlist)
    productsdf.to_csv(searchterm+ 'output.csv', index=False)
    print('saved to csv')


def scrape_all_pages(searchterm,max_pages=20):
    all_products = []
    page = 1

    while page <= max_pages:
        print(f"scraping page {page}...")
        soup = get_data(searchterm, page)
        products = parse(soup)

        if not products:
            break


        all_products.extend(products)
        page += 1

    return all_products    

productlist = scrape_all_pages(searchterm, max_pages=20)
output(productlist, searchterm)
print(productlist)

print(f'Total products scraped: {len(productlist)}')

