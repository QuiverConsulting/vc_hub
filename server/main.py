from fastapi import FastAPI
from get_vc_funding_data import *

app = FastAPI()


@app.get("/vc_funding_data")
async def root():
    return get_funding_data()
