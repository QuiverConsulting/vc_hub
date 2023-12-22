FROM python:3.12.1
COPY ./main.py ./
COPY ./get_vc_funding_data.py ./
COPY ./scraper.py ./
# COPY ./.env ./

RUN pip install requests beautifulsoup4 python-dotenv pymongo pydantic DateTime typing urllib3 regex fastapi uvicorn apscheduler python-dateutil
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
