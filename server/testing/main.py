import glob
import os
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
import numpy as np


cv = CountVectorizer(stop_words="english", max_features=1000, max_df=0.5, min_df=2)

all_names = set(names.words())
lemmatizer = WordNetLemmatizer()


def is_letter_only(word: str):
    return word.isalpha()


def clean_text(docs):
    docs_cleaned = []
    for doc in docs:
        doc = doc.lower()
        doc_cleaned = ' '.join(lemmatizer.lemmatize(word) for word in
                                doc.split() if is_letter_only(word))
        docs_cleaned.append(doc_cleaned)
    return docs_cleaned



emails, labels = [], []
file_path = 'enron1/spam/'

for filename in glob.glob(os.path.join(file_path, "*.txt")):
    with open(filename, 'r', encoding="ISO-8859-1") as infile:
        emails.append(infile.read())
        labels.append(1)


file_path = "enron1/ham/"
for filename in glob.glob(os.path.join(file_path, "*.txt")):
    with open(filename, 'r', encoding="ISO-8859-1") as infile:
        emails.append(infile.read())
        labels.append(0)


print(len(labels), len(emails))
emails_cleaned = clean_text(emails)
docs_cv = cv.fit_transform(emails_cleaned)

terms = cv.get_feature_names_out()
print(terms[932])


def get_label_index(labels):
    label_index = defaultdict(list)
    for index, label in enumerate(labels):
        label_index[label].append(index)
    return label_index


label_index = get_label_index(labels)
print(label_index)


def get_prior(label_index):

    prior = {label: len(index) for label, index in label_index.items()}
    total_count = sum(prior.values())
    for label in prior:
        prior[label] /= float(total_count)
    return prior


prior = get_prior(label_index)
print("Prior: ",  prior)


def get_likelihood(term_matrix, label_index, smoothing=0):
    likelihood = {}
    for label, index in label_index.items():
        likelihood[label] = term_matrix[index, : ].sum(axis=0) + smoothing
        likelihood[label] = np.array(likelihood[label])[0]
        total_count = likelihood[label].sum()
        likelihood[label] = likelihood[label] / float(total_count)
    return likelihood


smoothing = 1
likelihood = get_likelihood(docs_cv, label_index, smoothing=smoothing)
print(len(likelihood[0]))


def get_posterior(term_matrix, prior, likelhood):
    num_docs = term_matrix.shape[0]
    posteriors = []
    for i in range(num_docs):
        ...


