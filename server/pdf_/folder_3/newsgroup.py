from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.manifold import TSNE

import seaborn as sns
import matplotlib.pyplot as plt

categories = ['talk.religion.misc', 'comp.graphics', 'sci.space']
groups = fetch_20newsgroups(categories=categories)


def is_letter_only(word):
    for char in word:
        if not char.isalpha():
            return False

    return True


def fetch_groups(categories: list, random_state: int = 42):
    return fetch_20newsgroups(categories=categories, random_state=random_state)


def create_tsne_model(
                      data,
                      n_components: int = 2,
                      perplexity: int = 40,
                      random_state: int = 42,
                      learning_rate: int = 500
                      ):
    # topics are all over the place, which means
    # they are contextually similar
    tsne_model = TSNE(n_components=2,  # The output dimension
                      perplexity=40,  # nearest data points considered neighbors
                      random_state=42,
                      learning_rate=500,
                      )
    data_tsne = tsne_model.fit_transform(new_count_vector.toarray())
    plt.scatter(data_tsne[:, 0], data_tsne[:, 1], c=groups.target)
    plt.show()


"""
print(groups.keys())
print(groups["target_names"])
print(groups["target"])

sns.displot(groups.target)
# plt.show()
"""

all_names = set(names.words())
count_vector = CountVectorizer(max_features=500, stop_words="english")
lemmatizer = WordNetLemmatizer()


data_cleaned = []
count_vector_sw = CountVectorizer(stop_words="english", max_features=500)

for doc in groups.data:
    doc_cleaned = " ".join(
        lemmatizer.lemmatize(word)
        for word in doc.split()
        if is_letter_only(word) and word not in all_names
    )
    data_cleaned.append(doc_cleaned)

new_count_vector = count_vector_sw.fit_transform(data_cleaned)


