import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from textblob import TextBlob
from langchain_ollama.llms import OllamaLLM
from langchain.chains.llm import LLMChain
from langchain import PromptTemplate
import json


class RssAnalyzer:
    df: pd.DataFrame

    def __init__(self, llm_model: str = "llama3.2:1b"):
        self.nlp = spacy.load("en_core_web_lg")
        self.analyzer = SentimentIntensityAnalyzer()
        self.ollama_llm = OllamaLLM(model=llm_model)

    def llm_check_if_positive(self, text: str):
        """
            N == Negative
            P == Positive
            A == Neutral
            We use this letters to map the choicefield on Rss model
        """

        prompt = f"""
            You are a sentiment analysis expert. Analyze the following text and determine if it's positive or negative.

            Text: "{text}"

            Reply with ONLY ONE of these exact words: POSITIVE or NEGATIVE or NEUTRAL

            Just the word, nothing else.
        """

        # Get response from LLM
        response = self.ollama_llm.invoke(prompt).strip().upper()
        return "P" if response == "POSITIVE" else "N" if response == "NEGATIVE" else "A"

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




