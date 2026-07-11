import requests
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read API key
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")


def check_virustotal(url):
    try:
        if not API_KEY:
            print("VirusTotal API key not found")
            return None

        headers = {
            "x-apikey": API_KEY
        }

        # Submit URL for analysis
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if response.status_code != 200:
            print("VirusTotal submit failed:", response.text)
            return None

        analysis_id = response.json()["data"]["id"]

        # Get analysis report
        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        if report.status_code != 200:
            print("VirusTotal report failed:", report.text)
            return None

        stats = report.json()["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        # Total detections
        return malicious + suspicious

    except Exception as e:
        print("VirusTotal Error:", e)
        return None


def virustotal_risk_score(detections):
    if detections is None:
        return 0
    elif detections >= 5:
        return 40
    elif detections >= 1:
        return 20
    else:
        return 0
    