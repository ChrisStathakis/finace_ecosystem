import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy



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
        print(vs)
        return "N" if vs['neg'] > 0.6 else "P" if vs['pos'] > 0.6 else "A"


    def finbert_sentimental_analysis(self, text):
        # Load the tokenizer and model for FinBERT
        model_name = "yiyanghkust/finbert-tone"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Initialize the sentiment-analysis pipeline
        sentiment_model = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        return sentiment_model(text)




