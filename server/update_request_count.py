# to be triggered from scraper and get_vc_funding_data, shuts down the lambdas if threshold is met
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import sys

load_dotenv()
logging.basicConfig(level=logging.getLevelName(os.getenv('LOGGING_LEVEL')), format="[%(levelname)s | %(asctime)s | %(filename)s:%(lineno)s] : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

MONGO_CONNECTION_STR = os.getenv('DB_CONNECTION_STR')
DB_NAME = os.getenv('DB_NAME')
DB_REQUEST_COUNT_COLLECTION = os.getenv('DB_REQUEST_COUNT_COLLECTION')


def update_request_count():
    client = MongoClient(MONGO_CONNECTION_STR)
    try:
        db = client[DB_NAME]
        collection = db[DB_REQUEST_COUNT_COLLECTION]
        # TODO: update counter in db +2 (this lambda + the one that called it)
        logging.info(f"Incremented request counter.")
    except Exception as e:
        logging.error(f"Error while updating request counter: {e}.")
    finally:
        client.close()


def check_request_count():
    # TODO: check request count from db
    # if threshold is met
    shutdown_lambdas()


def shutdown_lambdas():
    pass


def main(args=None):
    update_request_count()
    check_request_count()


if __name__ == '__main__':
    main(sys.argv[1:])
