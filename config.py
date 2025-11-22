import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

    # Verification thresholds
    # CONFIDENCE_THRESHOLD = 0.6      # You can tune this
    # MISINFO_WEIGHT = 0.3            # How harshly misinfo keywords drop score
    # TRUST_BONUS = 0.4               # How much trusted domains boost score
