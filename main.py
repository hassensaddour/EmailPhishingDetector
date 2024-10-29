from email_analyzer.report import analyze_email
import joblib
import numpy as np

# main.py


# Load the model and vectorizers
model = joblib.load('ml_model/phishing_detector_model.pkl')
sender_vectorizer = joblib.load('ml_model/sender_vectorizer.pkl')
subject_vectorizer = joblib.load('ml_model/subject_vectorizer.pkl')
body_vectorizer = joblib.load('ml_model/body_vectorizer.pkl')


def classify_email(sender, subject, body, urls):
    # Vectorize input features
    sender_tfidf = sender_vectorizer.transform([sender]).toarray()
    subject_tfidf = subject_vectorizer.transform([subject]).toarray()
    body_tfidf = body_vectorizer.transform([body]).toarray()
    urls_array = np.array([[urls]])

    # Combine features
    X = np.hstack([sender_tfidf, subject_tfidf, body_tfidf, urls_array])
    prediction = model.predict(X)

    return "Phishing" if prediction == 1 else "Legitimate"


# Test the classifier
result = classify_email("bank@secure.com", "Urgent action required", "Please verify your account", 1)
print(f"The email is classified as: {result}")
