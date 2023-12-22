from fastapi import FastAPI
from get_vc_funding_data import *
from scraper import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI()

@app.get("/vc_funding_data")
async def root():
    return get_funding_data()


def populateDb():
    try:
        insert_db(scrape())
        logging.info("ran successfully")
    except Exception as e:
        logging.error(f"Error while scraping data: {e}")


@app.on_event("startup")
async def schedule_periodic():
    app.scheduler = AsyncIOScheduler()
    app.scheduler.add_job(populateDb, 'cron', hour="6", minute="0") # add 5 hours for UTC time diff, executes at 1am
    app.scheduler.start()
