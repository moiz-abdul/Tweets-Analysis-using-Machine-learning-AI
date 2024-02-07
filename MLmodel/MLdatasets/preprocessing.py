import pandas as pd
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Load your dataset
df = pd.read_csv('labeled_politicaltweets.csv')

# Define a function for text cleaning
def clean_text(tweet_text):
    # Remove special characters, URLs, and other noise
    tweet_text = re.sub(r'http\S+', '', tweet_text)  # Remove URLs
    tweet_text = re.sub(r'[^a-zA-Z\s]', '', tweet_text)  # Remove special characters
    return tweet_text

# Apply text cleaning to the 'tweet_text' column
df['cleaned_text'] = df['tweet_text'].apply(clean_text)

# Tokenization
df['tokens'] = df['cleaned_text'].apply(word_tokenize)

# Text Vectorization using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=10000)  # You can adjust the number of features
X_tfidf = tfidf_vectorizer.fit_transform(df['cleaned_text'])

# Now X_tfidf contains the numerical features representing the text data
# You can merge these features back into your DataFrame if needed
# For example:
df = pd.concat([df, pd.DataFrame(X_tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names_out())], axis=1)

# Save the preprocessed dataset to a new CSV file
df.to_csv('preprocessed_tweet_dataset.csv', index=False)
