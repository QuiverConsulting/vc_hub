import os
import requests
import logging
from bs4 import BeautifulSoup
from enum import Enum
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
MONGO_CONNECTION_STR = os.getenv('DB_CONNECTION_STR')
DB_NAME = os.getenv('DB_NAME')
DB_COLLECTION = os.getenv('DB_COLLECTION')

currency = ["$", "€", "£", "¥"]


class Article(BaseModel):
    company_name: Optional[str]
    funding: Optional[str]
    location: Optional[str]
    series: Optional[str]
    financiers: Optional[List[str]]
    date: Optional[str]
    link: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.now)


class Sites(Enum):
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
    Sites.SIFTED: 'https://sifted.eu/sector/venture-capital',
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
        parse_html(page.text, site)


def parse_html(html_data, site):
    # there are different parsers that we can use besides html.parser
    soup = BeautifulSoup(html_data, "html.parser")
    match site.value:
        case Sites.TECHRUNCH_STARTUPS.value:
            articles = parse_articles(soup, "div", "post-block post-block--image post-block--unread",
                                      "time")
            print(articles)
        case Sites.TECHCRUNCH_VENTURE.value:
            articles = parse_articles(soup, "div", "post-block post-block--image post-block--unread",
                                      "time")
            print(articles)
        case Sites.CRUNCHBASE.value:
            articles = parse_articles(soup, "article", ["herald-lay-b", "herald-lay-f"],
                                      date_class="updated")
            print(articles)
        case Sites.CRUNCHBASE_SEED.value:
            articles = parse_articles(soup, "article", ["herald-lay-a", "herald-lay-c", "herald-lay-f"],
                                      date_class="updated")
            print(articles)
        case Sites.EUSTARTUPS.value:
            # TODO: handle duplicate articles
            articles = parse_articles(soup, "div", "td-animation-stack", "time")
            print(articles)
        case Sites.SIFTED.value:
            articles = parse_articles(soup, "li", "m-0",
                                      date_class="whitespace-nowrap text-[14px] leading-4 text-[#5b5b5b]")
            # print(articles)

        case Sites.FINSMES.value:
            articles = parse_articles(soup, article_tag="article", date_tag="time")
            print(articles)
 #TODO: create list of Article objects, populate each object and call to add to db

def parse_articles(soup, article_tag, article_class=None, date_tag=None, date_class=None, link_class=None):
    articles = []
    kwargs_article = dict(name=article_tag, class_=article_class)
    kwargs_date = dict(name=date_tag, class_=date_class)
    kwargs_link = dict(name='a', class_=link_class)

    articles_parsed = soup.find_all(**{k: v for k, v in kwargs_article.items() if v is not None})
    for article in articles_parsed:
        for character in article.text:
            if character in currency:  # Only parse articles that have currency in content
                data = tokenize(article.text)  # Run article text through NER model
                company_name = parse_orgs(data)  # Get company name
                location = parse_location(data)  # Get location
                financiers = parse_financiers(data)  #Get list of financiers

                date_parse = article.findNext(**{k: v for k, v in kwargs_date.items() if v is not None})
                if date_tag == 'time':
                    date = date_parse['datetime']
                else:
                    date = date_parse.text

                link_parsed = article.findNext(**{k: v for k, v in kwargs_link.items() if v is not None})
                link = link_parsed['href']
                articles.append(Article(article=article.getText(separator=" ", strip=True), link=link, date=date,
                 company_name=company_name, series='test series', location=location,
                 funding='$10000', financiers=financiers))

                break  # Prevent re-running for every character in for loop if ran once

    for test in articles:
        print(test)
    return articles

def tokenize(article):
    API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    data = query(article)

    return data

def parse_orgs(data):

    orgs = []
    for entry in data:
        if entry['entity_group'] == 'ORG' and not isVC(entry['word']):
            orgs.append(entry['word'])

    if len(orgs) == 0:
        return None

    return orgs[0]   #TODO: Figure out how to handle multiple orgs that aren't investors


def isVC(organization):

    #query list of known VCs on startup and check in there
    keywords = ['VC', 'Capital', 'Venture', 'Partner']

    for word in keywords:
        if word in organization:
            return True

    return False

def parse_financiers(data):

    financiers = []
    for entry in data:
        if entry['entity_group'] == 'ORG' and isVC(entry):
            financiers.append(entry['word'])

    if len(financiers) == 0:
        return None

    return financiers
def parse_location(data):
    locations = []
    for entry in data:
        if entry['entity_group'] == 'LOC':
            locations.append(entry['word'])

    if len(locations) == 0:
        return None

    return locations[0]

# def parse_funding(article):

def insert_db(articles):
    client = MongoClient(MONGO_CONNECTION_STR)
    try:
        db = client[DB_NAME]
        collection = db[DB_COLLECTION]
        collection.insert_many(articles)
        logging.info(f"Inserted {len(articles)} records into db.")
    except Exception as e:
        logging.error(f"Error while inserting to db: {e}\n articles: {articles}.")


if __name__ == '__main__':
    scrape()
    a1 = Article(article='test article', link='test link', date='test date',
                 company_name='test company name', series='test series', location='test location',
                 funding='$10000', financiers=['financer1', 'financer2'])

    a2 = Article(article='test article2', link='test link2', date='test date2',
                 company_name='test company name2', series=None, location='test location2',
                 funding='$100002', financiers=['financer12', 'financer22'])
    # insert_db([a1.model_dump(), a2.model_dump()])
