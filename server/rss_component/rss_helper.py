import pandas
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from tickers.models import Ticker
import glob, os
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, recall_score, f1_score, precision_score, classification_report
from sklearn.model_selection import StratifiedKFold







class RssMachineLearning:
    emails = []
    labels = []

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.clf = MultinomialNB(alpha=1.0, fit_prior=True)
        self.cv = CountVectorizer(stop_words="english", max_features=1000, max_df=5, min_df=2)

    def load_data(self, filepath :str, label: int):
        for filename in glob.glob(os.path.join(filepath, "*.txt")):
            with open(filename, 'r', encoding="ISO-8859-1") as infile:
                self.emails.append(infile.read())
                self.labels.append(label)

    def clean_text(self):
        lemmatizer = self.lemmatizer
        docs_cleaned = []
        for doc in self.emails:
            doc = doc.lower()
            doc_cleaned = ' '.join(lemmatizer.lemmatize(word) for word in
                                   doc.split() if self.is_letter_only(word))
            docs_cleaned.append(doc_cleaned)

        return docs_cleaned

    def train_data(self):
        data_cleaned = self.clean_text()
        X_train, X_test, Y_train, Y_test = train_test_split(data_cleaned,
                                                            self.labels,
                                                            test_size=0.33,
                                                            random_state=42
                                                            )
        term_docs_train = self.cv.fit_transform(X_train)
        term_docs_test = self.cv.fit_transform(Y_train)
        self.clf.fit(term_docs_train, Y_train)
        prediction_prob = self.clf.predict_proba(term_docs_test)
        print(prediction_prob[0:10])

        prediction = self.clf.predict(term_docs_test)
        print(prediction[:10])
        accuracy = self.clf.score(term_docs_test, Y_test)
        print(f'Accuracy: {accuracy*100} %')
        conf_matrix = confusion_matrix(Y_test, prediction, labels=[0, 1])
        print(conf_matrix)
        precision = precision_score(Y_test, prediction, pos_label=1) # Precision measures the fraction of positive calls that are correct
        recall = recall_score(Y_test, prediction, pos_label=1) # Recall, on the other hand, measures the fraction of true positives that are correctly identified
        f1 = f1_score(Y_test, prediction, pos_label=1)

        print(classification_report(Y_test, prediction))

    def k_fold(self, n_splits=10):
        k_fold = StratifiedKFold(n_splits=n_splits, random_state=42)
        return k_fold

    @staticmethod
    def is_letter_only(word: str):
        return word.isalpha()

class WordEditor:
    result = []

    def __init__(self, sentence: str):
        self.sentence = sentence
        nltk.download('stopwords')

    def create_words(self):
        tokens = word_tokenize(self.sentence)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if not word in stop_words]
        self.result = tokens

    def stem_data(self):
        porter = PorterStemmer()
        stems = []
        for word in self.result:
            stems.append(porter.stem(word))
        self.result = stems

    def cross_tickers(self):
        tickers = []
        for word in self.result:
            qs = self.find_tickers(word)

            if qs.exists():
                for ticker in qs:
                    tickers.append(ticker)
        print(self.result)
        print(tickers)
        return tickers


    @staticmethod
    def find_tickers(word: str):
        search_vector = SearchVector('title', 'ticker')
        search_query = SearchQuery(word)

        qs = Ticker.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
            search=word
        ).order_by("-rank")

        return qs
