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
    #        SITES.TECHRUNCH_STARTUPS: 'https://techcrunch.com/category/startups/',
    #        SITES.TECHCRUNCH_VENTURE: 'https://techcrunch.com/category/venture/',
    #        SITES.CRUNCHBASE: 'https://news.crunchbase.com/',
    #        SITES.CRUNCHBASE_SEED: 'https://news.crunchbase.com/sections/seed/',
    #        SITES.EUSTARTUPS: 'https://www.eu-startups.com/category/fundin/',
             SITES.SIFTED: 'https://sifted.eu/sector/venture-capital',
    #        SITES.FINSMES: 'https://www.finsmes.com/'
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


def parse_article(data, article_tag, article_class=None, date_tag=None, date_class=None, link_class=None):
    articles = []
    kwargs_article = dict(name=article_tag, class_=article_class)
    kwargs_date = dict(name=date_tag, class_=date_class)
    kwargs_link = dict(name='a', class_=link_class)

    articles_parsed = data.find_all(**{k: v for k, v in kwargs_article.items() if v is not None})
    for article in articles_parsed:
        date_parse = article.findNext(**{k: v for k, v in kwargs_date.items() if v is not None})
        if date_tag == 'time':
            date = date_parse['datetime']
        else:
            date = date_parse.text

        link_parsed = article.findNext(**{k: v for k, v in kwargs_link.items() if v is not None})
        link = link_parsed['href']
        articles.append({'date': date, 'article': article.getText(separator=" ", strip=True), 'link': link})
    return articles


def parse(html_data, site):
    # there are different parsers that we can use besides html.parser
    parsed_data = BeautifulSoup(html_data, "html.parser")
    match site.value:
        case SITES.TECHRUNCH_STARTUPS.value:
            articles = parse_article(parsed_data, "div", "post-block post-block--image post-block--unread",
                                              "time")
            print(articles)
        case SITES.TECHCRUNCH_VENTURE.value:
            articles = parse_article(parsed_data, "div", "post-block post-block--image post-block--unread",
                                              "time")
            print(articles)
        case SITES.CRUNCHBASE.value:
            articles = parse_article(parsed_data, "article", ["herald-lay-b", "herald-lay-f"],
                                              date_class="updated")
            print(articles)
        case SITES.CRUNCHBASE_SEED.value:
            articles = parse_article(parsed_data, "article", ["herald-lay-a", "herald-lay-c", "herald-lay-f"],
                                              date_class="updated")
            print(articles)
        case SITES.EUSTARTUPS.value:
            # TODO: handle duplicate articles
            articles = parse_article(parsed_data, "div", "td-animation-stack", "time")
            print(articles)
        case SITES.SIFTED.value:
            articles = parse_article(parsed_data, "li", "m-0",
                                              date_class="whitespace-nowrap text-[14px] leading-4 text-[#5b5b5b]")
            #print(articles)
            for article in articles:
                content = article['article']
                for character in content:
                    if character in currency:
                        tokenize(content)
                        break
        case SITES.FINSMES.value:
            articles = parse_article(parsed_data, article_tag="article", date_tag="time")
            print(articles)


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
