import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read Google Safe Browsing API key
API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")


def check_safe_browsing(url):
    try:
        if not API_KEY:
            print("Google Safe Browsing API key not found")
            return False

        endpoint = (
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
        )

        payload = {
            "client": {
                "clientId": "sentriguard-ai",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }

        response = requests.post(endpoint, json=payload)

        if response.status_code != 200:
            print("Safe Browsing API Error:", response.text)
            return False

        data = response.json()

        # If "matches" exists, Google found the URL suspicious
        return "matches" in data

    except Exception as e:
        print("Safe Browsing Error:", e)
        return False


def safe_browsing_risk_score(is_malicious):
    if is_malicious:
        return 50
    return 0
