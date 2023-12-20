# lambda endpoint for our frontend to get the vc funding data
import os
from dotenv import load_dotenv
import logging
import update_request_count

load_dotenv()
logging.basicConfig(level=logging.getLevelName(os.getenv('LOGGING_LEVEL')), format="[%(levelname)s | %(asctime)s | %(filename)s:%(lineno)s] : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

def get_funding_data():
    pass

if __name__ == '__main__':
    try:
        get_funding_data()
    except Exception as e:
        logging.error(f"Error while getting data: {e}")
    finally:
        update_request_count.main()
