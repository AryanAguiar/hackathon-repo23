import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def search_claim_on_google(claim_text):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": claim_text,
        "num": 5
    }

    res = requests.get(url, params=params)
    data = res.json()

    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"],
            })
    return results
