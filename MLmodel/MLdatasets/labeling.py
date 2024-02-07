import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from joblib import dump
from joblib import load

# Step 1: Load the sentiment analysis dataset (e.g., CSV file)
sentiment_dataset = pd.read_csv("SentimentAnalysis.csv")


# Handle NaN values by filling them with an empty string
sentiment_dataset['clean_text'] = sentiment_dataset['clean_text'].fillna("")


# Step 3: Split the dataset into features (X) and labels (y)
X = sentiment_dataset['clean_text']
y = sentiment_dataset['category']

# Step 4: Create a TF-IDF vectorizer for text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Step 5: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle NaN values in labels
X_train = X_train[~y_train.isna()]  # Remove rows with NaN labels
y_train = y_train.dropna()

# Step 6: Train a machine learning model (e.g., Support Vector Machine) on the sentiment dataset
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Step 7: Evaluate the model's accuracy on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Step 8: Save the trained model for future use
dump(model, 'sentiment_model.joblib')
dump(vectorizer, 'tfidf_vectorizer.joblib')

# Now you have a trained sentiment analysis model and vectorizer.

# Step 9: Load the new dataset that you want to label
new_dataset = pd.read_csv("political_tweets.csv")

# Load the trained model and vectorizer
model = load('sentiment_model.joblib')
vectorizer = load('tfidf_vectorizer.joblib')

# Step 10: Preprocess the new dataset (similar to the sentiment dataset)
new_dataset['tweet_text'] = new_dataset['tweet_text'].fillna("")
# Step 12: Predict sentiment labels for tweets
new_dataset['tweet_category'] = model.predict(vectorizer.transform(new_dataset['tweet_text']))


# Step 13: Save the new_dataset with predicted labels
new_dataset.to_csv("labeled_politicaltweets.csv", index=False)