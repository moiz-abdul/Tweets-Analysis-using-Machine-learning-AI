import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

# Load the dataset from the CSV file
dataset = pd.read_csv('labeled_politicaltweets.csv')

# Tokenization and stemming
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Create a list to store preprocessed data
preprocessed_data = []

def preprocess_text(text):
    if isinstance(text, str):
        # Tokenization
        words = word_tokenize(text)

        # Removing stopwords and stemming
        filtered_words = [stemmer.stem(w.lower()) for w in words if w.lower() not in stop_words]

        return ' '.join(filtered_words)
    else:
        return ''  # Handle cases where text is not a string


# Preprocess the entire dataset
for index in range(len(dataset)):
    entry_data = {}
    
    entry_data['Original Tweet'] = dataset['tweet_text'].iloc[index]
    entry_data['Preprocessed Tweet'] = preprocess_text(entry_data['Original Tweet'])
    
    entry_data['Original Comments'] = []
    entry_data['Preprocessed Comments'] = []
    for i in range(1, 6):
        comment = dataset[f'comment_{i}'].iloc[index]
        entry_data['Original Comments'].append(comment)
        entry_data['Preprocessed Comments'].append(preprocess_text(comment))

    preprocessed_data.append(entry_data)

# Create a new DataFrame with preprocessed data
preprocessed_data_df = pd.DataFrame(preprocessed_data)

# Save the preprocessed data to a new CSV file
preprocessed_data_df.to_csv('preprocessed_politicatweets.csv', index=False)
