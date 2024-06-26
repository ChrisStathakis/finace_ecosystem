import nltk
from nltk.corpus import movie_reviews
import random


# Load movie reviews from NLTK corpus
nltk.download('movie_reviews')
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

# Shuffle the documents
random.shuffle(documents)

# Define the word features
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

# Function to find features in the document


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


# Extract features for all documents
featuresets = [(document_features(d), c) for (d,c) in documents]

# Split the data into training and testing sets
train_set, test_set = featuresets[100:], featuresets[:100]

# Train a Naive Bayes classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Test the classifier
print(nltk.classify.accuracy(classifier, test_set))

# Example usage
phrase = "Bitcoin rally continues as cryptocurrency tops $65,000"
features = document_features(phrase.split())
print("Positive" if classifier.classify(features) == 'pos' else "Negative")

import pandas as pd

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/philipperemy/financial-news-dataset/master/all-data.csv", header=None, names=["Label", "Headline"])

# Display the first few rows of the dataset
print(df.head())

# Example usage
phrase = "Stocks rise as company earnings beat expectations"
print("Positive" if classifier.classify(document_features(phrase.split())) == 'pos' else "Negative")