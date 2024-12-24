from sklearn.cluster import KMeans
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from sklearn import datasets
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np

from utilities import is_letter_only


categories = [
    "alt.atheism",
    "talk.religion.misc",
    "comp.graphics",
    "sci.space"
]

lemmatizer = WordNetLemmatizer()
groups = fetch_20newsgroups(subset="all", categories=categories)
labels = groups.target
labels_names = groups.target_names
all_names = set(names.words())


data_cleaned = []
for doc in groups.data:
    doc = doc.lower()
    doc_cleaned = " ".join(lemmatizer.lemmatize(word) for word in doc.split()
                           if is_letter_only(word)
                           and word not in all_names
                           )
    data_cleaned.append(doc_cleaned)

count_vector = CountVectorizer(stop_words="english", max_features=None, max_df=0.5, min_df=2)
tfidf_vector = TfidfVectorizer(stop_words="english", max_features=None, max_df=0.5, min_df=2)
data = count_vector.fit_transform(data_cleaned)
data2 = tfidf_vector.fit_transform(data_cleaned)


k = 4
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans2 = KMeans(n_clusters=k, random_state=42)
kmeans.fit_transform(data)
kmeans2.fit_transform(data2)
clusters = kmeans.labels_
clusters2 = kmeans2.labels_

print("------------------------ clusters---------------------------")
print(Counter(clusters))
print("------------------------ clusters2---------------------------")
print(Counter(clusters2))

cluster_label = {i: labels[np.where(clusters == i)] for i in range(k)}
terms = tfidf_vector.get_feature_names_out()
centroids = kmeans2.cluster_centers_


for cluster, index_list in cluster_label.items():
    counter = Counter(cluster_label[cluster])
    print(f"Cluster: {cluster} => Samples: {len(index_list)}")
    for label_index, count in sorted(counter.items(), key=lambda x: x[1], reverse=True):
        print(f"{labels_names[label_index]}: {count}")
        print("Top 10:")
        for ind in centroids[cluster].argsort()[-10:]:
            print(' %s' % terms[ind], end="")
        print()

print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")


t = 20
nmf = NMF(n_components=t, random_state=42)
nmf.fit(data2)
nmf_terms = tfidf_vector.get_feature_names_out()
for topic_idx, topic in enumerate(nmf.components_):
    print(f"Topic {topic_idx}:")
    print(" ".join(([terms[i] for i in topic.argsort()[-10:]])))


lda = LatentDirichletAllocation(n_components=t, learning_method="batch", random_state=42)
lda.fit(data2)

print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")


for topic_idx, topic in enumerate(lda.components_):
    print("Topic {}:" .format(topic_idx))
    print(" ".join([terms[i] for i in topic.argsort()[-10:]]))

    # 105