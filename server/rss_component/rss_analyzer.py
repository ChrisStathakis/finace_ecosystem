import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score
import spacy
from tabulate import tabulate

class RssAnalyzer:
    df: pd.DataFrame

    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download("averaged_perceptron_tagger")
        self.ps = PorterStemmer()
        self.nlp = spacy.load("en_core_web_lg")


    def find_tickers(self, title: str):
        doc = self.nlp(title)
        usefull_data = []
        for ent in doc.ents:
            usefull_data.append(ent.text)

        return usefull_data

    def load_dataset(self):
        data = pd.read_csv("rss_component/databases/data.csv")
        data['Sentence'] = data['Sentence'].apply(self.remove_html_tags)
        data['Sentence'] = data['Sentence'].apply(self.clean_text)
        self.df = data


    def train_dataset(self):
        data = self.df
        cv = CountVectorizer(max_features=5000)
        le = LabelEncoder()
        trf = le.fit_transform(data[['Sentiment']])
        trf = pd.DataFrame(trf)

        data = self.df
        data['Sentiment'] = trf
        vectors = cv.fit_transform(data['Sentence'])
        vectors = vectors.toarray()
        print(vectors)

        X = vectors
        y = data['Sentiment']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2
        )

        gnb = GaussianNB()
        mnb = MultinomialNB()
        bnb = BernoulliNB()

        mnb.fit(X_train, y_train)
        y_preds = mnb.predict(X_test)
        return mnb, cv

    def predict_rss(self, rss):
        mnb, cv = self.train_dataset()

        new_data = [f"{rss.title}"]
        new_data_proc = [self.preprocess_text(text) for text in new_data]
        new_data_vec = cv.transform(new_data_proc)
        predictions = mnb.predict(new_data_vec)
        return True if 1 in predictions else False

    @staticmethod
    def clean_text(text: str):
        ps = PorterStemmer()
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(text)
        transformed_text = []
        for w in words:
            if w.isalnum():
                transformed_text.append(w.lower())

        cleaned_text = []
        for w in transformed_text:
            stemmed_word = ps.stem(w)
            if stemmed_word not in stop_words:
                cleaned_text.append(stemmed_word)
        return " ".join(cleaned_text)

    @staticmethod
    def preprocess_text(text: str):
        stop_words = set(stopwords.words("english"))
        tokens = [word for word in text.lower().split() if word not in stop_words]
        return " ".join(tokens)

    @staticmethod
    def remove_html_tags(text: str):
        clean_text = re.compile("<.*?>")
        return re.sub(clean_text, " ", text)



