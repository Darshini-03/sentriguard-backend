import whois
from datetime import datetime
from urllib.parse import urlparse

from .ssl_checker import check_ssl, ssl_risk_score
from .threat_intel import check_virustotal, virustotal_risk_score
from .safe_browsing import check_safe_browsing, safe_browsing_risk_score


# ==========================================
# DOMAIN AGE ANALYSIS USING WHOIS
# ==========================================

def get_domain_age(url):
    try:
        # Extract domain
        domain = urlparse(url).netloc

        if domain.startswith("www."):
            domain = domain[4:]

        # WHOIS lookup
        w = whois.whois(domain)

        creation_date = w.creation_date

        # Handle list response
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # If date unavailable
        if not creation_date:
            return None

        # Fix timezone issue
        if hasattr(creation_date, "tzinfo") and creation_date.tzinfo is not None:
            creation_date = creation_date.replace(tzinfo=None)

        age = (datetime.now() - creation_date).days

        return age

    except Exception as e:
        print("WHOIS Error for", url, ":", e)
        return None



# ==========================================
# DOMAIN AGE RISK SCORE
# ==========================================

def domain_age_score(age):

    if age is None:
        return 0

    if age < 30:
        return 40

    elif age < 180:
        return 20

    else:
        return 0



# ==========================================
# COMPLETE URL ANALYSIS
# ==========================================

def analyze_url(url):

    # 1. Domain Age
    # Disabled during validation because WHOIS is slow
    # Enabled separately during real-time scanning

    age = None
    domain_score = 0


    # 2. SSL Certificate Check
    ssl_valid = check_ssl(url)
    ssl_score = ssl_risk_score(ssl_valid)


    # 3. VirusTotal Check
    detections = check_virustotal(url)
    vt_score = virustotal_risk_score(detections)


    # 4. Google Safe Browsing Check
    google_flagged = check_safe_browsing(url)
    google_score = safe_browsing_risk_score(google_flagged)


    # 5. Total Risk Score

    total_score = (
        domain_score +
        ssl_score +
        vt_score +
        google_score
    )


    # 6. Final Verdict

    if total_score >= 70:

        verdict = "Fraudulent Website"

    elif total_score >= 20:

        verdict = "Suspicious Website"

    else:

        verdict = "Likely Genuine Website"



    return {

        "url": url,

        # WHOIS
        "domain_age_days": age,
        "domain_risk_score": domain_score,


        # SSL
        "ssl_valid": ssl_valid,
        "ssl_risk_score": ssl_score,


        # VirusTotal
        "virustotal_detections": detections,
        "virustotal_risk_score": vt_score,


        # Google Safe Browsing
        "google_safe_browsing_flagged": google_flagged,
        "google_safe_browsing_risk_score": google_score,


        # Final
        "total_risk_score": total_score,
        "verdict": verdict
    }
