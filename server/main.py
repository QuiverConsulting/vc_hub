from fastapi import FastAPI
from get_vc_funding_data import *

from scraper import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

NEXT_SCRAPE_DATE = None

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/vc_funding_data")
async def root():
    return {"articles": get_funding_data(), "expiry_date": NEXT_SCRAPE_DATE}


def populateDb():
    try:
        global NEXT_SCRAPE_DATE
        NEXT_SCRAPE_DATE = datetime.datetime.now() + datetime.timedelta(days=1)
        insert_db(scrape())
        logging.info("ran successfully")
    except Exception as e:
        logging.error(f"Error while scraping data: {e}")


@app.on_event("startup")
async def schedule_periodic():
    app.scheduler = AsyncIOScheduler()
    app.scheduler.add_job(populateDb, 'cron', hour=os.getenv('CRON_HOUR'), minute="0")
    app.scheduler.start()
