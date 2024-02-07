import pandas as pd
import joblib  # To load the model and vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

# Load the saved Random Forest Classifier model and TF-IDF vectorizer
model = joblib.load('random_forest_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Input features for the unseen tweet
input_text = " Promoting ghost farmers. Let's invest in a world where spirits tend to our crops and harvests.  #GhostFarmers"


input_comment_count = 368
input_retweets_count = 278
input_likes_count = 232

input_views_count = 30600

input_tweet_category = 0

input_sentiment_score = 0.75



# Vectorize the tweet text using TF-IDF
X_tfidf = tfidf_vectorizer.transform([input_text])

# Combine the TF-IDF features with other numeric features
X_numeric = pd.DataFrame({
    'likes_count': [input_likes_count],
    'retweets_count': [input_retweets_count],
    'comment_count': [input_comment_count],
    'views_count': [input_views_count],
    'tweet_category': [input_tweet_category]
})
X_combined = hstack([X_tfidf, X_numeric])

# Predict whether the unseen tweet is real or fake
prediction = model.predict(X_combined)

if prediction[0] == 1:
    print("This Tweet is classified as REAL.")
else:
    print("This Tweet is classified as FAKE.")
