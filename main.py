from fastapi import FastAPI
import requests
import os

app = FastAPI()

SAM_API_KEY = os.getenv("SAM_API_KEY")  # Use environment variable for security
SAM_BASE_URL = "https://api.sam.gov/prod/opportunities/v2/search"

@app.get("/")
def root():
    return {"message": "SAM.gov API is running!"}

@app.get("/get_sam_tenders")
def get_sam_tenders(keyword: str):
    params = {
        "api_key": SAM_API_KEY,
        "q": keyword,
        "limit": 10  # Adjust as needed
    }
    response = requests.get(SAM_BASE_URL, params=params)
    return response.json()

