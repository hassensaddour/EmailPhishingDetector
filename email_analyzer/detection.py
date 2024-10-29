import re

def detect_suspicious_keywords(text):
    suspicious_keywords = ['urgent', 'password', 'reset', 'click here', 'account suspended']
    return [kw for kw in suspicious_keywords if kw in text.lower()]

def detect_suspicious_links(body):
    urls = re.findall(r'http[s]?://[^\s]+', body)
    return urls

def detect_suspicious_attachments(msg):
    suspicious_extensions = ['.exe', '.zip', '.scr', '.bat', '.jar']
    suspicious_attachments = []
    for part in msg.walk():
        if part.get_content_maintype() == 'application' and part.get_filename():
            file_extension = part.get_filename().split('.')[-1]
            if f'.{file_extension.lower()}' in suspicious_extensions:
                suspicious_attachments.append(part.get_filename())
    return suspicious_attachments
