import email
import numpy as np
from .parser import parse_email
from .detection import detect_suspicious_keywords, detect_suspicious_links, detect_suspicious_attachments
from email_analyzer.link_analysis import check_domain_reputation, check_redirects, is_matching_domain, extract_domain
import joblib  # Import joblib to load your ML model

# Load the ML model and vectorizers at the start
model = joblib.load('ml_model/phishing_detector_model.pkl')
sender_vectorizer = joblib.load('ml_model/sender_vectorizer.pkl')
subject_vectorizer = joblib.load('ml_model/subject_vectorizer.pkl')
body_vectorizer = joblib.load('ml_model/body_vectorizer.pkl')


def classify_email_ml(sender, subject, body, urls):
    # Vectorize input features
    sender_tfidf = sender_vectorizer.transform([sender]).toarray()
    subject_tfidf = subject_vectorizer.transform([subject]).toarray()
    body_tfidf = body_vectorizer.transform([body]).toarray()
    urls_array = np.array([[urls]])

    # Combine features
    X = np.hstack([sender_tfidf, subject_tfidf, body_tfidf, urls_array])
    prediction = model.predict(X)

    return "Phishing" if prediction == 1 else "Legitimate"


def analyze_email(raw_email):
    parsed_email = parse_email(raw_email)
    print("Parsed Email:", parsed_email)  # Debugging line

    report = {
        'Subject': parsed_email['subject'],
        'From': parsed_email['from'],
        'Suspicious Keywords': detect_suspicious_keywords(parsed_email['body']),
        'Suspicious Links': detect_suspicious_links(parsed_email['body']),
        'Suspicious Attachments': detect_suspicious_attachments(email.message_from_string(raw_email)),
        'Link Analysis': {},
        'ML Classification': ''
    }

    print("Suspicious Keywords Detected:", report['Suspicious Keywords'])  # Debugging line
    print("Suspicious Links Detected:", report['Suspicious Links'])  # Debugging line

    # Analyze each link for reputation and redirection
    for link in report['Suspicious Links']:
        domain = extract_domain(link)
        domain_report = check_domain_reputation(domain)
        redirect_info = check_redirects(link)
        domain_match = is_matching_domain(parsed_email['from'], link)

        report['Link Analysis'][link] = {
            'Domain Reputation': domain_report,
            'Redirect Info': redirect_info,
            'Domain Match': domain_match
        }

    # Classify the email using ML
    report['ML Classification'] = classify_email_ml(parsed_email['from'], parsed_email['subject'], parsed_email['body'],
                                                    len(report['Suspicious Links']))

    risk_score = len(report['Suspicious Keywords']) + len(report['Suspicious Links']) + len(
        report['Suspicious Attachments'])
    report['Phishing Risk'] = "High" if risk_score >= 2 else "Medium" if risk_score == 1 else "Low"

    return report
