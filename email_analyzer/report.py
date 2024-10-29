import email
from .parser import parse_email
from .detection import detect_suspicious_keywords, detect_suspicious_links, detect_suspicious_attachments

def analyze_email(raw_email):
    parsed_email = parse_email(raw_email)
    report = {
        'Subject': parsed_email['subject'],
        'From': parsed_email['from'],
        'Suspicious Keywords': detect_suspicious_keywords(parsed_email['body']),
        'Suspicious Links': detect_suspicious_links(parsed_email['body']),
        'Suspicious Attachments': detect_suspicious_attachments(email.message_from_string(raw_email))
    }
    risk_score = len(report['Suspicious Keywords']) + len(report['Suspicious Links']) + len(report['Suspicious Attachments'])
    report['Phishing Risk'] = "High" if risk_score >= 2 else "Medium" if risk_score == 1 else "Low"
    return report
