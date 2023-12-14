import os
import requests
import logging
from bs4 import BeautifulSoup
from enum import Enum
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
DB_PASS = os.getenv('DB_PASS')
DB_USER = os.getenv('DB_USER')

currency = ["$", "€", "£", "¥"]
class SITES(Enum):
    GEEKWIRE = 'geekwire'
    TECHRUNCH_STARTUPS = 'teachcrunch_startups'
    TECHCRUNCH_VENTURE = 'techcrunch_venture'
    CRUNCHBASE = 'crunchbase'
    CRUNCHBASE_SEED = 'crunchbase_seed'
    EUSTARTUPS = 'eustartups'
    SIFTED = 'sifted'
    FINSMES = 'finsmes'

sites = {
#        SITES.GEEKWIRE: 'https://www.geekwire.com/fundings/',
        SITES.TECHRUNCH_STARTUPS: 'https://techcrunch.com/category/startups/',
#        SITES.TECHCRUNCH_VENTURE: 'https://techcrunch.com/category/venture/',
#        SITES.CRUNCHBASE: 'https://news.crunchbase.com/',
#        SITES.CRUNCHBASE_SEED: 'https://news.crunchbase.com/sections/seed/',
#        SITES.EUSTARTUPS: 'https://www.eu-startups.com/category/fundin/',
#      SITES.SIFTED: 'https://sifted.eu/sector/venture-capital',
#         SITES.FINSMES: 'https://www.finsmes.com/'
}


def scrape():
    if not os.path.exists('htmlFiles'):
        os.makedirs('htmlFiles')
    for site in sites:
        logging.info(f'Scraping {sites[site]}...')
        page = requests.get(sites[site], headers={'User-Agent': 'VC_HUB'})

        with open(f"htmlFiles/html_{site.value}.txt", 'w', encoding="utf-8") as html_file:
            html_file.write(page.text)
        logging.info(f'Parsing {sites[site]}...')
        parse(page.text, site)


def parse(html_data, site):
    # there are different parsers that we can use besides html.parser
    parsed_data = BeautifulSoup(html_data, "html.parser")
    match site.value:
        case SITES.TECHRUNCH_STARTUPS.value:
            articles = parsed_data.find_all("div", class_ ="post-block post-block--image post-block--unread")
            for article in articles:
                date = article.findNext("time")
                print(date['datetime'])
                print(article.getText(separator=" ", strip=True))
                print('\n')
        case SITES.TECHCRUNCH_VENTURE.value:
            articles = parsed_data.find_all("div", class_="post-block post-block--image post-block--unread")
            for article in articles:
                print(article.getText(separator=" ", strip=True))
                print('\n')
        case SITES.CRUNCHBASE.value:
            articles = parsed_data.find_all("article", class_=["herald-lay-b","herald-lay-f"])
            for article in articles:
                print(article.getText(separator=" ", strip=True))
                print('\n')
        case SITES.CRUNCHBASE_SEED.value:
            articles = parsed_data.find_all("article", class_=["herald-lay-a","herald-lay-c","herald-lay-f"])
            for article in articles:
                print(article.getText(separator=" ", strip=True))
                print('\n')
        case SITES.EUSTARTUPS.value:
            # TODO: handle duplicate articles
            articles = parsed_data.find_all("div", class_="td-animation-stack")
            for article in articles:
                print(article.getText(separator=" ", strip=True))
                print('\n')
        case SITES.SIFTED.value:
            articles = parsed_data.find_all("li", class_="m-0")
            for article in articles:
                # print(article.getText(separator=" ", strip=True))
                # print('\n')
                content = article.getText(separator=" ", strip=True)
                for character in content:
                    if character in currency:
                        tokenize(content)
                        break
        case SITES.FINSMES.value:
            articles = parsed_data.find_all("article")
            for article in articles:
                date = article.findNext("time")
                print(date['datetime'])
                print(article.getText(separator=" ", strip=True))
                print('\n')


def tokenize(article):
    API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    data = query(article)
    print(data)
def insert_db():
    pass

if __name__ == '__main__':
    scrape()

