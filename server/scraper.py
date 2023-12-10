import requests
import logging
logging.basicConfig(level = logging.INFO)

sites = {
    'geekwire': 'https://www.geekwire.com/fundings/',
    'teachcrunch_startups': 'https://techcrunch.com/category/startups/',
    'techcrunch_venture': 'https://techcrunch.com/category/venture/',
    'crunchbase':'https://news.crunchbase.com/',
    'crunchbase_seed': 'https://news.crunchbase.com/sections/seed/',
    'eustartups':'https://www.eu-startups.com/category/fundin/',
    'sifted':'https://sifted.eu/sector/venture-capital',
    'finsmes':'https://www.finsmes.com/'
}

def scrape():
    for site in sites:
        logging.info(f'Scraping {sites[site]}...')
        page = requests.get(sites[site], headers={'User-Agent': 'VC_HUB'})
        with open(f"html_{site}.txt", 'w', encoding="utf-8") as html_file:
            html_file.write(page.text)

if __name__ == '__main__':
    scrape()
