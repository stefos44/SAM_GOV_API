from fastapi import FastAPI
import requests

app = FastAPI()

SAM_API_KEY = "QZpVzWvccKghhC5AoxY4A1ljOUrp5E5ve2uEwO1h"
SAM_BASE_URL = "https://api.sam.gov/prod/opportunities/v2/search"

@app.get("/get_sam_tenders")
def get_sam_tenders(keyword: str):
    params = {
        "api_key": SAM_API_KEY,
        "q": keyword,
        "limit": 10  # Number of results to fetch
    }
    response = requests.get(SAM_BASE_URL, params=params)
    return response.json()

