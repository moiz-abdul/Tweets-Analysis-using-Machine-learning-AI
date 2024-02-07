# tweetprediction.py
import os
from django.conf import settings
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

# Get the base directory of the Django project
BASE_DIR = settings.BASE_DIR

# Define the path to the model file
model_file_path = os.path.join(BASE_DIR, 'MLmodel', 'MLdatasets', 'random_forest_model.pkl')

# Load the model using the correct path
model = joblib.load(model_file_path)

# Load the saved Random Forest Classifier model and TF-IDF vectorizer
model = joblib.load('MLmodel/MLdatasets/random_forest_model.pkl')
tfidf_vectorizer = joblib.load('MLmodel/MLdatasets/tfidf_vectorizer.pkl')

def predict_tweet(tweet_text, likes_count, retweets_count, comment_count, views_count):
    # Vectorize the tweet text using TF-IDF
    X_tfidf = tfidf_vectorizer.transform([tweet_text])

    # Combine the TF-IDF features with other numeric features
    X_numeric = pd.DataFrame({
        'likes_count': [likes_count],
        'retweets_count': [retweets_count],
        'comment_count': [comment_count],
        'views_count': [views_count],
        'tweet_category': [0]  # Assuming a default value for tweet_category
    })
    X_combined = hstack([X_tfidf, X_numeric])

    # Predict whether the unseen tweet is real or fake
    prediction = model.predict(X_combined)

    return prediction
