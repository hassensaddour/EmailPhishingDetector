from bs4 import BeautifulSoup
import re

def detect_suspicious_keywords(text):
    suspicious_keywords = ['urgent', 'password', 'reset', 'click here', 'account suspended', 'Your account will be locked unless you act now', 'Please complete these steps to avoid account closure',
                          'Your billing information is out of date. You will be fined!', 'Dangerous new virus detected on your system', 'Get free Bitcoin in your account', 'Earn money while working from home']
    return [kw for kw in suspicious_keywords if kw in text.lower()]

def detect_suspicious_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return [link for link in links if re.search(r'(bit\.ly|tinyurl|unknown-domain)', link)]

def detect_suspicious_attachments(msg):
    suspicious_extensions = ['.exe', '.zip', '.scr', '.bat', '.jar']
    suspicious_attachments = []
    for part in msg.walk():
        if part.get_content_maintype() == 'application' and part.get_filename():
            file_extension = part.get_filename().split('.')[-1]
            if f'.{file_extension.lower()}' in suspicious_extensions:
                suspicious_attachments.append(part.get_filename())
    return suspicious_attachments
