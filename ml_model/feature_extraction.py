from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def vectorize_text(data):
    # Initialize TF-IDF vectorizers for sender, subject, and body
    sender_vectorizer = TfidfVectorizer(max_features=100)
    subject_vectorizer = TfidfVectorizer(max_features=100)
    body_vectorizer = TfidfVectorizer(max_features=300)

    # Transform sender, subject, and body fields
    sender_tfidf = sender_vectorizer.fit_transform(data['sender']).toarray()
    subject_tfidf = subject_vectorizer.fit_transform(data['subject']).toarray()
    body_tfidf = body_vectorizer.fit_transform(data['body']).toarray()

    # Combine TF-IDF features with urls feature
    urls_array = data['urls'].values.reshape(-1, 1)
    X = np.hstack([sender_tfidf, subject_tfidf, body_tfidf, urls_array])

    return X, sender_vectorizer, subject_vectorizer, body_vectorizer
