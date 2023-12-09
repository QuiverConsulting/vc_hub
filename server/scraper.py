import logging
import requests

sites = [
    'https://www.geekwire.com/fundings/'
    #'https://techcrunch.com/category/startups/',
    #'https://techcrunch.com/category/venture/',
    #'https://news.crunchbase.com/',
    #'https://news.crunchbase.com/sections/seed/',
    #'https://www.eu-startups.com/category/fundin/',
    #'https://sifted.eu/sector/venture-capital',
    #'https://www.finsmes.com/'
]

def scrape():
    for site in sites:
        page = requests.get(site)
        print(page.text)

if __name__ == '__main__':
    scrape()
