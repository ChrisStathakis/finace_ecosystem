import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from textblob import TextBlob


class RssAnalyzer:
    df: pd.DataFrame

    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.analyzer = SentimentIntensityAnalyzer()

    def find_entities(self, text: str):
        """
            Using spacy to find entities
        """
        doc = self.nlp(text)
        usefull_data = []
        for ent in doc.ents:
            usefull_data.append(ent.text)
        return usefull_data

    def sentimental_analysis_text(self, text: str):
        """
            N == Negative
            P == Positive
            A == Neutral
            We use this letters to map the choicefield on Rss model
        """

        vs = self.analyzer.polarity_scores(text)
        return "N" if vs['neg'] > 0.6 else "P" if vs['pos'] > 0.6 else "A"


    def textblob_sentimental_analysis(self, text):
        # textblob sentimental_analysis
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        return "P" if sentiment > 0 else "N" if sentiment < 0  else "A"




