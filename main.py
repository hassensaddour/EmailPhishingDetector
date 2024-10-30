# main.py
from email_analyzer.report import analyze_email


if __name__ == "__main__":
    # Load a sample email for testing
    with open('sample_emails/sample_email.eml', 'r') as f:
        raw_email = f.read()

    # Run phishing analysis
    phishing_report = analyze_email(raw_email)

    print("Phishing Report:")
    for key, value in phishing_report.items():
        if key == 'Link Analysis':
            for link, link_info in value.items():
                print(f"Link: {link}")
                print(f"  Domain Reputation: {link_info['Domain Reputation']}")
                print(f"  Redirect Info: {link_info['Redirect Info']}")
                print(f"  Domain Match: {link_info['Domain Match']}")
        elif key == 'NLP Analysis':
            print("\nNLP Analysis:")
            for nlp_key, nlp_value in value.items():
                print(f"  {nlp_key}: {nlp_value}")
        else:
            print(f"{key}: {value}")
