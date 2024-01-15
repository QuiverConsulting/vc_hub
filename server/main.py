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
    return get_funding_data()


def populateDb():
    try:
        insert_db(scrape(), datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1))
        logging.info("Scraper ran successfully")
    except Exception as e:
        logging.error(f"Error while scraping data: {e}")


@app.get("/wake_up", include_in_schema=False)
async def root():
    return "Container woken up successfully"


@app.on_event("startup")
async def schedule_periodic():
    app.scheduler = AsyncIOScheduler()
    app.scheduler.add_job(populateDb, 'cron', hour=os.getenv('CRON_HOUR'), minute="0")
    app.scheduler.start()
    for job in app.scheduler.get_jobs():
        logging.info("Scraper will run next at: " + job.next_run_time)
