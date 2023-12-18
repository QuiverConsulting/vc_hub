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
import urllib.parse

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
MONGO_CONNECTION_STR = os.getenv('DB_CONNECTION_STR')
DB_NAME = os.getenv('DB_NAME')
DB_COLLECTION = os.getenv('DB_COLLECTION')

currencies = ["$", "€", "£", "¥"]


class Article(BaseModel):
    company_name: Optional[str]
    currency: Optional[str]
    funding: Optional[int]
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


def geekwire_airtable_scrape():
    # get access policy and request id
    url = 'https://airtable.com/app4aeBWKz5zcH0Fd/shrDVedlKm56eYymz/tblCYUF5t4ysJ8QDY'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    page = requests.get(url, headers=headers)
    try:
        access_policy = page.text.split('accessPolicy=')[1].split('"')[0]
        request_id = page.text.split('requestId: ')[1].split('"')[1]
    except Exception as e:
        logging.error(f"Error while finding access policy or request Id for Geekwire's airtable: {e}")
        return

    # get table data
    url = 'https://airtable.com/v0.3/view/viwFGZJAxhd0l0nWG/readSharedViewData'
    params = {'requestId': request_id, 'accessPolicy': f'{urllib.parse.unquote(access_policy)}'}
    headers = {'x-airtable-application-id': 'app4aeBWKz5zcH0Fd',
               'x-requested-with': 'XMLHttpRequest', 'x-time-zone': 'America/Toronto'}

    response = requests.get(url, headers=headers, params=params)

    json_data = response.json()
    columns = json_data['data']['columns']

    column_ids = {'company_id': next(col for col in columns if col["name"] == 'Company')['id'],
                  'date_id': next(col for col in columns if col["name"] == 'Date')['id'],
                  'amount_id': next(col for col in columns if col["name"] == 'Amount')['id'],
                  'series_id': next(col for col in columns if col["name"] == 'Series')['id'],
                  'leader_investor_id': next(col for col in columns if col["name"] == 'Lead Investor')['id'],
                  'coverage_id': next(col for col in columns if col["name"] == 'Coverage')['id']
                  }

    articles = []
    for row in json_data['data']['rows']:
        company_name = row['cellValuesByColumnId'][column_ids['company_id']] if column_ids['company_id'] in row[
            'cellValuesByColumnId'] else None
        date = row['cellValuesByColumnId'][column_ids['date_id']] if column_ids['date_id'] in row[
            'cellValuesByColumnId'] else None
        funding = row['cellValuesByColumnId'][column_ids['amount_id']] if column_ids['amount_id'] in row[
            'cellValuesByColumnId'] else None

        series = row['cellValuesByColumnId'][column_ids['series_id']] if column_ids['series_id'] in row[
            'cellValuesByColumnId'] else None
        financiers = row['cellValuesByColumnId'][column_ids['leader_investor_id']].split(", ") if column_ids['leader_investor_id'] in row['cellValuesByColumnId'] else None
        link = row['cellValuesByColumnId'][column_ids['coverage_id']] if column_ids['coverage_id'] in row[
            'cellValuesByColumnId'] else None

        a = Article(company_name=company_name, funding=funding, series=series, financiers=financiers, link=link,
                    date=date, currency='$', location=None)
        articles.append(a.model_dump())
    return articles


def scrape():
    # if not os.path.exists('htmlFiles'):
    #     os.makedirs('htmlFiles')
    articles = []
    for site in sites:
        logging.info(f'Scraping {sites[site]}...')
        page = requests.get(sites[site], headers={'User-Agent': 'VC_HUB'})

        # with open(f"htmlFiles/html_{site.value}.txt", 'w', encoding="utf-8") as html_file:
        #     html_file.write(page.text)
        logging.info(f'Parsing {sites[site]}...')
        articles.extend(parse_html(page.text, site))
    articles.extend(geekwire_airtable_scrape())

    return articles


def parse_html(html_data, site):
    # there are different parsers that we can use besides html.parser
    soup = BeautifulSoup(html_data, "html.parser")
    articles = None
    match site.value:
        case Sites.TECHRUNCH_STARTUPS.value:
            articles = parse_articles(soup, "div", "post-block post-block--image post-block--unread",
                                      "time")
        case Sites.TECHCRUNCH_VENTURE.value:
            articles = parse_articles(soup, "div", "post-block post-block--image post-block--unread",
                                      "time")
        case Sites.CRUNCHBASE.value:
            articles = parse_articles(soup, "article", ["herald-lay-b", "herald-lay-f"],
                                      date_class="updated")
        case Sites.CRUNCHBASE_SEED.value:
            articles = parse_articles(soup, "article", ["herald-lay-a", "herald-lay-c", "herald-lay-f"],
                                      date_class="updated")
        case Sites.EUSTARTUPS.value:
            # TODO: handle duplicate articles
            articles = parse_articles(soup, "div", "td-animation-stack", "time")
        case Sites.SIFTED.value:
            articles = parse_articles(soup, "li", "m-0",
                                      date_class="whitespace-nowrap text-[14px] leading-4 text-[#5b5b5b]")
        case Sites.FINSMES.value:
            articles = parse_articles(soup, article_tag="article", date_tag="time")

    return articles


# TODO: create list of Article objects, populate each object and call to add to db

def parse_articles(soup, article_tag, article_class=None, date_tag=None, date_class=None, link_class=None):
    articles = []
    kwargs_article = dict(name=article_tag, class_=article_class)
    kwargs_date = dict(name=date_tag, class_=date_class)
    kwargs_link = dict(name='a', class_=link_class)

    articles_parsed = soup.find_all(**{k: v for k, v in kwargs_article.items() if v is not None})
    for article in articles_parsed:
        for character in article.text:
            if character in currencies:  # Only parse articles that have currency in content
                data = tokenize(article.text)  # Run article text through NER model
                company_name = parse_orgs(data)  # Get company name
                location = parse_location(data)  # Get location
                financiers = parse_financiers(data)  # Get list of financiers
                funding = parse_funding(article.text)

                date_parse = article.findNext(**{k: v for k, v in kwargs_date.items() if v is not None})
                if date_tag == 'time':
                    date = date_parse['datetime']
                else:
                    date = date_parse.text

                link_parsed = article.findNext(**{k: v for k, v in kwargs_link.items() if v is not None})
                link = link_parsed['href']

                a = Article(article=article.getText(separator=" ", strip=True), link=link, date=date,
                            company_name=company_name, series='test series', location=location,
                            funding=funding, financiers=financiers, currency=character)

                articles.append(a.model_dump())

                break  # Prevent re-running for every character in for loop if ran once

    # for test in articles
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

    return orgs[0]  # TODO: Figure out how to handle multiple orgs that aren't investors


def isVC(organization):
    # query list of known VCs on startup and check in there
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


def parse_funding(article):
    funding = ''
    for i in range(0, len(article)):
        if article[i] in currencies:
            i += 1
            while article[i].isdigit():
                funding += article[i]
                i += 1
            if article[i].isspace():
                i += 1
            if article[i].lower() == 'm':
                return int(funding) * 1000000
            if article[i].lower() == 'b':
                return int(funding) * 1000000000
            return int(funding)


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
    # a1 = Article(article='test article', link='test link', date='test date',
    #              company_name='test company name', series='test series', location='test location',
    #              funding='$10000', financiers=['financer1', 'financer2'])
    #
    # a2 = Article(article='test article2', link='test link2', date='test date2',
    #              company_name='test company name2', series=None, location='test location2',
    #              funding='$100002', financiers=['financer12', 'financer22'])
    # insert_db([a1.model_dump(), a2.model_dump()])
    insert_db(scrape())
