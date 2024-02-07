import pandas as pd
import numpy as np 
# Load the original dataset
dataset = pd.read_csv('labeled_politicaltweets.csv')

# Feature 1: Length of Tweet Text
dataset['Tweet_Text_Length'] = dataset['tweet_text'].apply(len)

# Replace NaN values with empty strings
dataset = dataset.fillna('')

# Feature 2: Length of Comment Texts (average of the 5 comments)
comment_cols = ['comment_1', 'comment_2', 'comment_3', 'comment_4', 'comment_5']
dataset['Avg_Comment_Text_Length'] = dataset[comment_cols].applymap(lambda x: len(str(x))).mean(axis=1)

# Feature 3: Presence of Keywords (Example keywords: 'fake', 'misinformation', 'real')
keywords = ['Government Verified', 'Authentic Information', 'Official Statement', 'Trusted Source',
            'Political Analysis', 'Fact-Checked', 'Reliable Data', 'Transparency', 'Non-Partisan',
            'Balanced Reporting', 'Official Announcement', 'Verified Source', 'Credible Data',
            'Government Report', 'Non-Biased Analysis', 'Unbiased Opinion', 'Accurate Statistics',
            'Peer-Reviewed', 'Policy Brief', 'Impartial Viewpoint', 'In-Depth Research',
            'Cross-Referenced Data', 'Expert Consensus', 'Grounded in Facts', 'Verified Integrity',
            'Hoax', 'Misinformation', 'Propaganda', 'False Claims', 'Manipulated Data', 'Unverified Reports',
            'Biased Narrative', 'Fabricated Quotes', 'Sensationalism', 'Conspiracy Theory',
            'Disinformation', 'Election Manipulation', 'Fabricated Data', 'Manipulated Photos',
            'Deceptive Campaign', 'Hoax Conspiracy', 'False Survey Results', 'Partisan Propaganda',
            'Misleading Quotes', 'Pseudoscience', 'Doctored Evidence', 'Fraudulent Claims', 'Spurious Sources',
            'Fabricated Incidents', 'Conspiracy Agenda']

for keyword in keywords:
    dataset[f'Has_{keyword}_Keyword'] = dataset['tweet_text'].str.contains(keyword, case=False).astype(int)


# Feature 4: Hashtags Count (in Tweet Text)
dataset['Hashtags_Count'] = dataset['tweet_text'].str.count('#')

# Feature 5: Mentions Count (in Tweet Text)
dataset['Mentions_Count'] = dataset['tweet_text'].str.count('@')

# Feature 6: Combined Engagement Score (sum of likes, retweets, and views)
dataset['Engagement_Score'] = dataset['likes_count'] + dataset['retweets_count'] + dataset['views_count']

# Save the updated dataset
dataset.to_csv('featureengineering_politicaltweets.csv', index=False)
