# lambda endpoint for our frontend to get the vc funding data
import os
from dotenv import load_dotenv
import logging
from pymongo import MongoClient

load_dotenv()
logging.basicConfig(level=logging.getLevelName(os.getenv('LOGGING_LEVEL')),
                    format="[%(levelname)s | %(asctime)s | %(filename)s:%(lineno)s] : %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')

MONGO_CONNECTION_STR = os.getenv('DB_CONNECTION_STR')
DB_NAME = os.getenv('DB_NAME')
DB_FUNDING_COLLECTION = os.getenv('DB_FUNDING_COLLECTION')


def get_funding_data():
    client = MongoClient(MONGO_CONNECTION_STR)
    entries = []
    try:
        db = client[DB_NAME]
        collection = db[DB_FUNDING_COLLECTION]
        count = 1
        logging.info("Successfully connected to db")

        for d in collection.find({},{"_id":0}).sort({ "$natural": 1} ):
            entries.append(d)
            logging.info(f"Appending to list {count}")
            count += 1

    except Exception as e:
        logging.error(f"Error while getting data: {e}")
        client.close()
        return f"Error while getting data: {e}"
    finally:
        client.close()
        logging.info("Returning info to FASTAPI")
        return entries

def test():
    return DB_NAME


if __name__ == '__main__':
    get_funding_data()