from fastapi import FastAPI, Query
import requests
import os
from datetime import datetime, timedelta

app = FastAPI()

SAM_API_KEY = os.getenv("SAM_API_KEY")
SAM_BASE_URL = "https://api.sam.gov/prod/opportunities/v2/search"

@app.get("/get_sam_tenders")
def get_sam_tenders(
    keyword: str,
    posted_from: str = Query(None, description="Start date (YYYY-MM-DD)"),
    posted_to: str = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(1000, description="Number of tenders to fetch (max 1000)")
):
    if not posted_from:
        posted_from = (datetime.utcnow() - timedelta(days=30)).strftime("%m/%d/%Y")
    else:
        posted_from = datetime.strptime(posted_from, "%Y-%m-%d").strftime("%m/%d/%Y")

    if not posted_to:
        posted_to = datetime.utcnow().strftime("%m/%d/%Y")
    else:
        posted_to = datetime.strptime(posted_to, "%Y-%m-%d").strftime("%m/%d/%Y")

    params = {
        "api_key": SAM_API_KEY,
        "keywords": keyword,  # ✅ Use "keywords" instead of "q"
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "limit": min(limit, 1000),
        "nocache": datetime.utcnow().strftime("%Y%m%d%H%M%S"),  # ✅ Prevent caching
        "start": 0  # ✅ Ensure you're getting the first set of tenders
    }

    response = requests.get(SAM_BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}
    
    data = response.json()

    tenders = [
        {
            "title": tender.get("title", "N/A"),
            "solicitationNumber": tender.get("solicitationNumber", "N/A"),
            "postedDate": tender.get("postedDate", "N/A"),
            "responseDeadline": tender.get("responseDeadLine", "N/A"),
            "naicsCode": tender.get("naicsCode", "N/A"),
            "uiLink": tender.get("uiLink", "N/A")
        }
        for tender in data.get("opportunitiesData", [])
    ]

    return {"total_tenders": data.get("totalRecords", 0), "tenders": tenders}
