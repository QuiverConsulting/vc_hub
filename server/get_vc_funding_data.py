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
NUM_FUNDING_ENTRIES = os.getenv('NUM_FUNDING_ENTRIES')
DB_EXPIRY_DATE_COLLECTION = os.getenv('DB_EXPIRY_DATE_COLLECTION')


def get_funding_data():
    client = MongoClient(MONGO_CONNECTION_STR)
    try:
        db = client[DB_NAME]
        collection = db[DB_FUNDING_COLLECTION]
        logging.info("Successfully connected to db")
        collection.create_index('date')
        data = list(collection.find({},{"_id":0}).sort({ "date": -1}).limit(int(NUM_FUNDING_ENTRIES)))
        collection = db[DB_EXPIRY_DATE_COLLECTION]
        expiry_date = collection.find_one({"title": "expiry_date"}, {'_id': 0})
        return {'articles': data, 'expiry_date': expiry_date['expiry_date']}

    except Exception as e:
        logging.error(f"Error while getting data: {e}")
        client.close()
        return {'articles': [], 'expiry_date': None}
    finally:
        client.close()
        logging.info("Returning info to FASTAPI")

# if __name__ == '__main__':
#     logging.info(len(get_funding_data()))