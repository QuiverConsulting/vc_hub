import os
import requests
import logging
from bs4 import BeautifulSoup
from enum import Enum

logging.basicConfig(level=logging.INFO)

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
#        SITES.TECHRUNCH_STARTUPS: 'https://techcrunch.com/category/startups/',
#        SITES.TECHCRUNCH_VENTURE: 'https://techcrunch.com/category/venture/',
#        SITES.CRUNCHBASE: 'https://news.crunchbase.com/',
#        SITES.CRUNCHBASE_SEED: 'https://news.crunchbase.com/sections/seed/',
#        SITES.EUSTARTUPS: 'https://www.eu-startups.com/category/fundin/',
#        SITES.SIFTED: 'https://sifted.eu/sector/venture-capital',
        SITES.FINSMES: 'https://www.finsmes.com/'
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
        case SITES.TECHCRUNCH_VENTURE.value:
            test = parsed_data.find_all("div", class_ ="post-block post-block--image post-block--unread")
            for entry in test:
                print(" ".join(entry.text.split()))
                print('\n')
        case SITES.FINSMES.value:
            test = parsed_data.find_all("article")
            for entry in test:
                print(entry.getText(separator=" ", strip=True))
                print('\n')



def insert_db():
    pass


if __name__ == '__main__':
    scrape()
