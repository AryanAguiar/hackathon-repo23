import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    query = "The Earth revolves around the Sun once every 365.25 days."