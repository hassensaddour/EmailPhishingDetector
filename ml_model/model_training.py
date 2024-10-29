import joblib
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from data_loader import load_data
from feature_extraction import vectorize_text

# Step 1: Load data
data = load_data('CEAS_08.csv')

# Step 2: Extract features and labels
X, sender_vectorizer, subject_vectorizer, body_vectorizer = vectorize_text(data)
y = data['label']

# Step 3: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 6: Save the model and vectorizers
joblib.dump(model, 'phishing_detector_model.pkl')
joblib.dump(sender_vectorizer, 'sender_vectorizer.pkl')
joblib.dump(subject_vectorizer, 'subject_vectorizer.pkl')
joblib.dump(body_vectorizer, 'body_vectorizer.pkl')
