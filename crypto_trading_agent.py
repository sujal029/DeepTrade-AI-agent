import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Download VADER lexicon if not available
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Load Dataset
try:
    df = pd.read_csv("C:\\Users\\baiss\\OneDrive\\Desktop\\portfolio\\pbc hackthon ai agent news app\\crypto_tweets_.csv")
    print("Dataset Loaded Successfully!")
except FileNotFoundError:
    print("Error: Dataset file not found. Check the file path.")
    exit()

# Preview dataset
print(df.head())

# Ensure correct column names
if 'tweet' not in df.columns or 'price_change' not in df.columns:
    print("Error: The dataset must have 'tweet' and 'price_change' columns.")
    exit()

# Text Preprocessing Function
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\@w+|\#', '', text)  # Remove mentions and hashtags
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)  # Remove special characters
    return text

df['cleaned_tweet'] = df['tweet'].apply(clean_text)

# Sentiment Analysis
df['sentiment_score'] = df['cleaned_tweet'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Features & Labels
X = df['cleaned_tweet']
y = df['price_change']

# Convert text to numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# Split data into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Train Machine Learning Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make Predictions
y_pred = model.predict(X_test)

# Evaluate Model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# **Make a Prediction on a New Tweet**
def predict_crypto_movement(tweet):
    cleaned_tweet = clean_text(tweet)
    vectorized_tweet = vectorizer.transform([cleaned_tweet])
    prediction = model.predict(vectorized_tweet)
    
    if prediction[0] == 1:
        return "📈 Price Up!"
    else:
        return "📉 Price Down!"

# Example Tweet Prediction
new_tweet = "Bitcoin is breaking all records! 🚀 #Crypto #Bitcoin"
prediction_result = predict_crypto_movement(new_tweet)
print("Tweet Prediction:", prediction_result)
