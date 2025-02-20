from fastapi import FastAPI, Query
import requests
import os
from datetime import datetime, timedelta

app = FastAPI()

SAM_API_KEY = os.getenv("SAM_API_KEY")
SAM_BASE_URL = "https://api.sam.gov/prod/opportunities/v2/search"

@app.get("/")
def root():
    return {"message": "SAM.gov API is running!"}

@app.get("/get_sam_tenders")
def get_sam_tenders(
    keyword: str,
    posted_from: str = Query(None, description="Start date (YYYY-MM-DD)"),
    posted_to: str = Query(None, description="End date (YYYY-MM-DD)")
):
    # If no dates are provided, default to last 7 days
    if not posted_from:
        posted_from = (datetime.utcnow() - timedelta(days=7)).strftime("%m/%d/%Y")
    else:
        posted_from = datetime.strptime(posted_from, "%Y-%m-%d").strftime("%m/%d/%Y")

    if not posted_to:
        posted_to = datetime.utcnow().strftime("%m/%d/%Y")
    else:
        posted_to = datetime.strptime(posted_to, "%Y-%m-%d").strftime("%m/%d/%Y")

    params = {
        "api_key": SAM_API_KEY,
        "q": keyword,
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "limit": 10
    }
    
    response = requests.get(SAM_BASE_URL, params=params)
    
    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}
    
    return response.json()
