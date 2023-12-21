FROM python:3.12.1
COPY main.py .
RUN pip install requests beautifulsoup4 python-dotenv pymongo pydantic logging enum DateTime typing urllib3 regex
ENTRYPOINT [“python”, “./main.py”]