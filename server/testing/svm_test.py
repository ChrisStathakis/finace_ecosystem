from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import GridSearchCV
from collections import Counter
import timeit

lemmatizer = WordNetLemmatizer()
tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=None)
svc = SVC(kernel="linear", C=1.0, random_state=42)
svc_libsvm = SVC(kernel='linear')
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


categories = None

data_train = fetch_20newsgroups(subset="train", categories=categories, random_state=42)
data_test = fetch_20newsgroups(subset="test", categories=categories, random_state=42)

cleaned_train = clean_text(data_train.data)
label_train = data_train.target
cleaned_test = clean_text(data_test.data)
label_test = data_test.target
term_docs_train = tfidf_vectorizer.fit_transform(cleaned_train)
term_docs_test = tfidf_vectorizer.transform(cleaned_test)

parameters = {'C': (0.1, 1, 10, 100)}
grid_search = GridSearchCV(svc_libsvm, parameters, n_jobs=-1, cv=5)

start_time = timeit.default_timer()
print("Starts")
grid_search.fit(term_docs_train, label_train)
print("--- %0.3fs seconds ---" % (timeit.default_timer() - start_time))
print(grid_search.best_params_)
print(grid_search.best_score_)

"""
svc.fit(term_docs_train, label_train)
prediction = svc.predict(term_docs_test)
acurracy = svc.score(term_docs_test, label_test)
print(f"Accuracy: {acurracy}")

report = classification_report(label_test, prediction)
print(report)

"""