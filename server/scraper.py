import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

sites = {
    'geekwire': 'https://www.geekwire.com/fundings/',
    'teachcrunch_startups': 'https://techcrunch.com/category/startups/',
    'techcrunch_venture': 'https://techcrunch.com/category/venture/',
    'crunchbase': 'https://news.crunchbase.com/',
    'crunchbase_seed': 'https://news.crunchbase.com/sections/seed/',
    'eustartups': 'https://www.eu-startups.com/category/fundin/',
    'sifted': 'https://sifted.eu/sector/venture-capital',
    'finsmes': 'https://www.finsmes.com/'
}


def scrape():
    for site in sites:
        logging.info(f'Scraping {sites[site]}...')
        page = requests.get(sites[site], headers={'User-Agent': 'VC_HUB'})
        with open(f"htmlFiles/html_{site}.txt", 'w', encoding="utf-8") as html_file:
            html_file.write(page.text)
        logging.info(f'Parsing {sites[site]}...')
        parse(page.text)


def parse(html_data):
    # there are different parsers that we can use besides html.parser
    parsed_data = BeautifulSoup(html_data, "html.parser")
    # print(parsed_data.prettify())


def insert_db():
    pass;


if __name__ == '__main__':
    scrape()
