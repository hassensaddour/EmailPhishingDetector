import requests
from config import VIRUSTOTAL_API_KEY
import tldextract

def check_domain_reputation(domain):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['last_analysis_stats']
        else:
            print("Failed to check domain reputation.")
            return None
    except requests.RequestException as e:
        print("Error checking domain reputation:", e)
        return None

# email_analyzer/link_analysis.py


def check_redirects(url):
    try:
        response = requests.get(url, allow_redirects=True)
        redirect_count = len(response.history)
        final_url = response.url
        return {"redirect_count": redirect_count, "final_url": final_url}
    except requests.RequestException as e:
        print("Error checking redirects:", e)
        return {"redirect_count": None, "final_url": None}

# email_analyzer/link_analysis.py


def extract_domain(url):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    return domain

def is_matching_domain(sender_email, url):
    sender_domain = sender_email.split('@')[-1]
    url_domain = extract_domain(url)
    return sender_domain == url_domain
