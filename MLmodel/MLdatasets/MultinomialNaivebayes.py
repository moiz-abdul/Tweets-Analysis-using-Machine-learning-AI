import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from scipy.sparse import hstack

# Load your preprocessed dataset
df = pd.read_csv('preprocessed_tweet_dataset.csv')

# Split the dataset into features (X) and the target (y)
X_text = df['tweet_text']  # Textual feature
X_numeric = df[['likes_count', 'retweets_count', 'comment_count', 'views_count']]

# Split the data into a training set and a test set
X_train_text, X_test_text, X_train_numeric, X_test_numeric, y_train, y_test = train_test_split(X_text, X_numeric, df['Is_RealTweet'], test_size=0.2, random_state=42)

# Vectorize the tweet_text using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=10000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train_text)
X_test_tfidf = tfidf_vectorizer.transform(X_test_text)

# Combine the TF-IDF features with other numeric features
X_train_final = hstack([X_train_tfidf, X_train_numeric])
X_test_final = hstack([X_test_tfidf, X_test_numeric])

# Train a Multinomial Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_final, y_train)

# Make predictions
y_pred = model.predict(X_test_final)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Print a classification report for more detailed evaluation
print(classification_report(y_test, y_pred))
