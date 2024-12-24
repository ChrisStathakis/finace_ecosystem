import glob
import os
import numpy as np
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from collections import defaultdict
from pdf_.folder_3.utilities import is_letter_only


all_names = set(names.words())
lemmatizer = WordNetLemmatizer()
cv = CountVectorizer(stop_words=None,
                     max_features=1000,
                     # max_df=2,
                     # min_df=0.5
                     )

emails, labels = [], []


def clean_text(docs):
    docs_cleaned = []
    for doc in docs:
        doc = doc.lower()
        doc_cleaned = " ".join(lemmatizer.lemmatize(word) for word in doc.split()
                                if is_letter_only(word)
                                and word not in all_names
                                )
        docs_cleaned.append(doc_cleaned)

    return docs_cleaned


for filename in glob.glob(os.path.join("enron1/spam", "*.txt")):
    with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
        emails.append(infile.read())
        labels.append(1)


for filename in glob.glob(os.path.join("enron1/ham", "*.txt")):
    with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
        emails.append(infile.read())
        labels.append(0)


email_cleaned = clean_text(emails)
docs_cv = cv.fit_transform(email_cleaned)
# print(docs_cv[0])  # (row index, term index) term_frequency

terms = cv.get_feature_names_out()
# print(terms[601])


def get_label_index(labels):
    label_index = defaultdict(list)
    for index, label in enumerate(labels):
        label_index[label].append(index)
    return label_index


def get_prior(label_index):
    prior = {
        label: len(index) for label, index in label_index.items()
    }
    total_count = sum(prior.values())
    for label in prior:
        prior[label] /= float(total_count)
    return prior


# 121
def get_likelihood(term_matrix, label_index: dict, smoothing=0):
    likelihood = {}
    for label, index in label_index.items():
        likelihood[label] = term_matrix[index, :].sum(axis=0) + smoothing
        likelihood[label] = np.array(likelihood[label])[0]
        total_count = likelihood[label].sum()
        likelihood[label] = likelihood[label]/ float(total_count)
    return likelihood


def get_posterior(term_matrix, prior, likelhood):
    num_docs = term_matrix.shape[0]
    posteriors = []
    for i in range(num_docs):
        # posterior is proportional to prior * likelihood
        # = exp(log(prior * likelihood))
        # = exp(log(prior) + log(likelihood))

        posterior = {key: np.log(prior_label) for key, prior_label in prior.items()}

        for label, likelihood_label in likelihood.items():
            term_document_vector = term_matrix.getrow(i)
            counts = term_document_vector.data
            indices = term_document_vector.indices

            for count, index in zip(counts, indices):

                posterior[label] += np.log(likelihood_label[index]) * count
                # exp(-1000):exp(-999) will cause zero division error,
                # however it equates to exp(0):exp(1)

            min_log_posterior = min(posterior.values())

            for label in posterior:

                try:
                    posterior[label] = np.exp(posterior[label] - min_log_posterior)
                except:
                    posterior[label] = float('inf')
                    # normalize so that all sums up to 1

            sum_posterior = sum(posterior.values())

            for label in posterior:
                if posterior[label] == float('inf'):
                    posterior[label] = 1.0
                else:
                    posterior[label] /= sum_posterior

        posteriors.append(posterior.copy())

    return posteriors

smoothing = 1
label_index = get_label_index(labels)
likelihood = get_likelihood(docs_cv, label_index, smoothing)
# print(likelihood[1][:5])
# print(likelihood[0][:5])

# print(get_prior(label_index))
# print(label_index)

test_email = [
'''Subject: flat screens hello ,
    please call or contact regarding the other flat screens  requested .
... trisha tlapek - eb 3132 b
... michael sergeev - eb 3132 a
... also the sun blocker that was taken away from eb 3131 a .
... trisha should two monitors also michael .
... thanks
... kevin moore''',
    '''Subject: let ' s stop the mlm insanity !
... still believe you can earn $ 100 , 000 fast in mlm ? get real !
... get emm , a brand new system that replaces mlm with something that
works !
... start earning 1 , 000 ' s now ! up to $ 10 , 000 per week doing
simple
... online tasks .
... free info - breakfree @ luxmail . com - type " send emm info " in
the
... subject box .
... this message is sent in compliance of the proposed bill section 301
. per
... section 301 , paragraph ( a ) ( 2 ) ( c ) of s . 1618 . further
transmission
... to you by the sender of this e - mail may be stopped at no cost to
you by
... sending a reply to : " email address " with the word remove in the
subject
... line .''',

]
"""
prior = get_prior(label_index)
emails_cleaned_test = clean_text(test_email)
print(emails_cleaned_test)
term_docs_test = cv.fit_transform(emails_cleaned_test)
posterior = get_posterior(term_docs_test, prior=prior, likelhood=likelihood)
print(posterior)
# 121
"""


X_train, X_test, Y_train, Y_test = train_test_split(
    email_cleaned, labels, test_size=0.33, random_state=42
)

terms_docs_train = cv.fit_transform(X_train)
label_index = get_label_index(Y_train)
prior = get_prior(label_index)
likelihood = get_likelihood(terms_docs_train, label_index, smoothing)
print(likelihood)

terms_docs_test = cv.fit_transform(X_test)
posterior = get_posterior(terms_docs_test, prior, likelihood)
correct = 0.0

for pred, actual in zip(posterior, Y_test):
    ...

