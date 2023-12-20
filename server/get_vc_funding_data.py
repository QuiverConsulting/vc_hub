# lambda endpoint for our frontend to get the vc funding data
import logging
import update_request_count
logging.basicConfig(level=logging.INFO)

def get_funding_data():
    pass

if __name__ == '__main__':
    try:
        get_funding_data()
    except Exception as e:
        logging.error(f"Error while getting data: {e}")
    finally:
        update_request_count.main()
