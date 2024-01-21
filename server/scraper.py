import os

import dateutil
import requests
import logging
from bs4 import BeautifulSoup
from enum import Enum
from dotenv import load_dotenv
from pymongo import UpdateOne
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel, Field
from typing import Optional, List
import urllib.parse
import re
from dateutil import parser
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.getLevelName(os.getenv('LOGGING_LEVEL')), format="[%(levelname)s | %(asctime)s | %(filename)s:%(lineno)s] : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')


API_URL = os.getenv('API_URL')
API_TOKEN = os.getenv('API_TOKEN')
MONGO_CONNECTION_STR = os.getenv('DB_CONNECTION_STR')
DB_NAME = os.getenv('DB_NAME')
DB_FUNDING_COLLECTION = os.getenv('DB_FUNDING_COLLECTION')
DB_EXPIRY_DATE_COLLECTION = os.getenv('DB_EXPIRY_DATE_COLLECTION')

currencies = {"$", "€", "£", "¥"}
keywords = {" raise ", " nabs ", " snaps ", " extends ", " raises ", " raised ", " secured ", " secures ", " receieves ", " received ", " closes ", " closed "}

class Article(BaseModel):
    company_name: Optional[str]
    company_score: Optional[float]
    currency: Optional[str]
    funding: Optional[int]
    location: Optional[str]
    series: Optional[str]
    financiers: Optional[List[str]]
    date: Optional[datetime]
    link: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.now)

    def __hash__(self):
        return hash((self.company_name, self.company_score, self.currency, self.funding, self.location, self.series, self.date, self.link, str(self.financiers)))

    def __eq__(self, other):
        return (
            self.company_name == other.company_name and
            self.company_score == other.company_score and
            self.currency == other.currency and
            self.funding == other.funding and
            self.location == other.location and
            self.series == other.series and
            self.date == other.date and
            self.link == other.link and
            str(self.financiers) == str(other.financiers)
        )


class Sites(Enum):
    TECHRUNCH_STARTUPS = 'teachcrunch_startups'
    TECHCRUNCH_VENTURE = 'techcrunch_venture'
    CRUNCHBASE = 'crunchbase'
    CRUNCHBASE_SEED = 'crunchbase_seed'
    EUSTARTUPS = 'eustartups'
    SIFTED = 'sifted'
    FINSMES = 'finsmes'


sites = {
            Sites.TECHRUNCH_STARTUPS: 'https://techcrunch.com/category/startups/',
            Sites.TECHCRUNCH_VENTURE: 'https://techcrunch.com/category/venture/',
            Sites.CRUNCHBASE: 'https://news.crunchbase.com/',
            Sites.CRUNCHBASE_SEED: 'https://news.crunchbase.com/sections/seed/',
            Sites.EUSTARTUPS: 'https://www.eu-startups.com/category/fundin/',
            Sites.SIFTED: 'https://sifted.eu/sector/venture-capital',
            Sites.FINSMES: 'https://www.finsmes.com/'
}


def geekwire_airtable_scrape():
    # get access policy and request id
    url = 'https://airtable.com/app4aeBWKz5zcH0Fd/shrDVedlKm56eYymz/tblCYUF5t4ysJ8QDY'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    page = requests.get(url, headers=headers)
    try:
        logging.info(f'Scraping {url}...')
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

    logging.info(f'Parsing {url}...')
    column_ids = {'company_id': next(col for col in columns if col["name"] == 'Company')['id'],
                  'date_id': next(col for col in columns if col["name"] == 'Date')['id'],
                  'amount_id': next(col for col in columns if col["name"] == 'Amount')['id'],
                  'series_id': next(col for col in columns if col["name"] == 'Series')['id'],
                  'lead_investor_id': next(col for col in columns if col["name"] == 'Lead Investor')['id'],
                  'coverage_id': next(col for col in columns if col["name"] == 'Coverage')['id']
                  }

    articles = []
    for row in json_data['data']['rows']:
        company_name = row['cellValuesByColumnId'][column_ids['company_id']] if column_ids['company_id'] in row[
            'cellValuesByColumnId'] else None
        date = parser.parse(row['cellValuesByColumnId'][column_ids['date_id']]) if column_ids['date_id'] in row[
            'cellValuesByColumnId'] else None
        funding = row['cellValuesByColumnId'][column_ids['amount_id']] if column_ids['amount_id'] in row[
            'cellValuesByColumnId'] else None

        series = row['cellValuesByColumnId'][column_ids['series_id']] if column_ids['series_id'] in row[
            'cellValuesByColumnId'] else None
        financiers = row['cellValuesByColumnId'][column_ids['lead_investor_id']].split(", ") if column_ids['lead_investor_id'] in row['cellValuesByColumnId'] else None
        link = row['cellValuesByColumnId'][column_ids['coverage_id']] if column_ids['coverage_id'] in row[
            'cellValuesByColumnId'] else None

        a = Article(company_name=company_name, funding=funding, series=series, financiers=financiers, link=link,
                    date=date, currency='$', location='USA', company_score=None)
        articles.append(a.model_dump())
    logging.debug(f"Got {len(articles)} articles from geekwire's airtable: {articles}")
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
    articles = []
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
            articles = parse_articles(soup, "div", "td-animation-stack", "time",None,"td-image-wrap")
        case Sites.SIFTED.value:
            articles = parse_articles(soup, "li", "m-0",
                                      date_class="whitespace-nowrap text-[14px] leading-4 text-[#5b5b5b]")
        case Sites.FINSMES.value:
            articles = parse_articles(soup, article_tag="article", date_tag="time")

    logging.debug(f"Got {len(articles)} articles from {site.value}: {articles}")
    return articles


def parse_articles(soup, article_tag, article_class=None, date_tag=None, date_class=None, link_class=None):
    article_set = set()
    kwargs_article = dict(name=article_tag, class_=article_class)
    kwargs_date = dict(name=date_tag, class_=date_class)
    kwargs_link = dict(name='a', class_=link_class)

    articles_parsed = soup.find_all(**{k: v for k, v in kwargs_article.items() if v is not None})
    for article in articles_parsed:
        for character in article.text:
            if character in currencies and any(keyWord in article.text.lower() for keyWord in keywords):  # Only parse articles that have currency in content
                # if any(keyWord in article.text.lower() for keyWord in keywords):

                try:
                    data = tokenize(article.text)  # Run article text through NER model
                    company = parse_orgs(data)
                    company_name = company[0]  # Get company name
                    company_score = company[1]
                    location = parse_location(data)  # Get location
                    financiers = parse_financiers(data)  # Get list of financiers
                    funding = parse_funding(article.text)
                    series = parse_series((article.text.lower()))

                    date_parse = article.findNext( ** {k: v
                    for k, v in kwargs_date.items() if v is not None})
                    if date_tag == 'time':
                        date = parser.parse(date_parse['datetime'])
                    else:
                        date = datetime.strptime(date_parse.text, "%B %d, %Y")

                    link_parsed = article.findNext(**{k: v for k, v in kwargs_link.items() if v is not None})
                    link = link_parsed['href']

                    a = Article(link=link, date=date,
                                company_name=company_name, series=series, location=location,
                                funding=funding, financiers=financiers, currency=character, company_score = company_score)
                    article_set.add(a)
                except Exception as e:
                    logging.error(e)
                    logging.error(f"The following article caused an error: {article.text}")
                break  # Prevent re-running for every character in for loop if ran once





    article_list = []
    for article in article_set:
        article_list.append(article.model_dump())
    return article_list

def tokenize(article):
    # API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    data = query(article)

    return data


def parse_orgs(data):
    orgs = []
    score = 0
    for entry in data:
        if entry['entity_group'] == 'ORG' and re.match(r'([\w\s]+)', entry['word']) and not isVC(entry['word']) and score < entry['score']:
            orgs.clear()
            orgs.append(entry['word'])
            orgs.append(entry['score'])
            score = entry['score']

    if len(orgs) == 0:
        return [None,None]

    return orgs  # TODO: Figure out how to handle multiple orgs that aren't investors


def isVC(organization):
    # query list of known VCs on startup and check in there
    keywords = ['VC', 'Capital', 'Venture', 'Partner']

    for word in keywords:
        if word in organization:
            return True

    return False


def parse_financiers(data):
    financiers = set()
    for entry in data:
        if entry['entity_group'] == 'ORG' and re.match(r'([\w\s]+)', entry['word']) and isVC(entry['word']):
            financiers.add(entry['word'])

    if len(financiers) == 0:
        return None

    return list(financiers)


def parse_location(data):
    locations = []
    for entry in data:
        if entry['entity_group'] == 'LOC' and entry['word'].isalpha():
            locations.append(entry['word'])

    if len(locations) == 0:
        return None

    return locations[0]


def parse_funding(article):
    funding = ''
    for i in range(0, len(article)):
        if article[i] in currencies:
            i += 1
            while article[i].isdigit() or article[i] == '.' or article[i] == ',':
                funding += article[i]
                i += 1
            if article[i].isspace():
                i += 1
            if article[i].lower() == 'k':
                return round(float(funding.replace(",","")) * 1000)
            if article[i].lower() == 'm':
                return round(float(funding.replace(",","")) * 1000000)
            if article[i].lower() == 'b':
                return round(float(funding.replace(",","")) * 1000000000)
            return round(float(funding.replace(",","")))

def parse_series(article):
    if " seed " in article:
        return "Seed"
    elif " series " in article:
        return "Series " + article[article.index(" series ")+8].upper()
    return None

def insert_db(articles, next_scrape_date: datetime):
    client = MongoClient(MONGO_CONNECTION_STR)
    try:
        db = client[DB_NAME]
        collection = db[DB_FUNDING_COLLECTION]
        collection.create_index('date')
        upserts = [UpdateOne({'link': a['link'], 'company_name': a['company_name']}, {'$setOnInsert': a}, upsert=True) for a in articles]
        result = collection.bulk_write(upserts)
        logging.info(f"Inserted {result.upserted_count} records into db. Found {result.matched_count} duplicate records.")
        try:
            collection = db[DB_EXPIRY_DATE_COLLECTION]
            collection.update_one({"title": "expiry_date"}, {"$set": {'expiry_date': next_scrape_date}}, upsert=True)
            logging.info(f"Updated expiry date in db to {next_scrape_date}.")
        except Exception as ex:
            logging.error(f"Error updating expiry date to {next_scrape_date}: {ex}")
    except Exception as e:
        logging.error(f"Error while inserting to db: {e}\n articles: {articles}.")
    finally:
        client.close()

# if __name__ == '__main__':
#     try:
#         insert_db(scrape(),datetime.now())
#     except Exception as e:
#         logging.error(f"Error while scraping data: {e}")
