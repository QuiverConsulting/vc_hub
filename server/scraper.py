import logging
import requests

sites = [
    # 'https://www.geekwire.com/fundings/'
    #'https://techcrunch.com/category/startups/',
    'https://techcrunch.com/category/venture/',
    #'https://news.crunchbase.com/',
    # 'https://news.crunchbase.com/sections/seed/',
    # 'https://www.eu-startups.com/category/fundin/',
    # 'https://sifted.eu/sector/venture-capital',
    #'https://www.finsmes.com/'
]

def scrape():
    for site in sites:
        # page = requests.get(site, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"})
        # print(page.content)
        url = "https://techcrunch.com/category/venture/"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

if __name__ == '__main__':
    scrape()
