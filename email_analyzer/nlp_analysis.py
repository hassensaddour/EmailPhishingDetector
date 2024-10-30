import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load NLP models
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()

# Predefined phishing-related phrases for intent detection
intent_phrases = {
    "verification": ["verify your account", "account verification", "confirm account"],
    "urgent": ["urgent", "immediate action", "attention required"],
    "unusual activity": ["unusual activity", "suspicious login", "unrecognized device"]
}

def extract_entities(text):
    """Extract brand or organization names from the text."""
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON"]]
    return entities

def detect_intent(text):
    """Detect intents like 'verification', 'urgent' and 'unusual activity'."""
    detected_intents = []
    for intent, phrases in intent_phrases.items():
        if any(phrase in text.lower() for phrase in phrases):
            detected_intents.append(intent)
    return detected_intents

def analyze_sentiment(text):
    """Analyze sentiment to detect threatening or urgent tone."""
    sentiment_scores = sentiment_analyzer.polarity_scores(text)
    if sentiment_scores['neg'] > 0.5 and sentiment_scores['compound'] < -0.3:
        return "Threatening"
    elif sentiment_scores['pos'] > 0.5:
        return "Positive"
    elif sentiment_scores['neu'] > 0.5:
        return "Neutral"
    return "Neutral"
