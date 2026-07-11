import whois
from datetime import datetime
from urllib.parse import urlparse


def get_domain_age(url):
    try:
        # Extract domain from URL
        domain = urlparse(url).netloc

        # Remove www.
        if domain.startswith("www."):
            domain = domain[4:]

        # Get WHOIS information
        w = whois.whois(domain)
        creation_date = w.creation_date

        # Handle list format
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # If no creation date available
        if not creation_date:
            return None

        # Calculate age in days
        age = (datetime.now() - creation_date).days
        return age

    except Exception as e:
        print("WHOIS Error:", e)
        return None


def domain_age_score(age):
    # If WHOIS information is unavailable, do not penalize the website
    if age is None:
        return 0

    # Very new domains are more suspicious
    if age < 30:
        return 40
    elif age < 180:
        return 20
    else:
        return 0
      