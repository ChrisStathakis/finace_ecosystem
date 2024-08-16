import spacy
import requests
from bs4 import BeautifulSoup


"""
Text: The original word text.
Lemma: The base form of the word.
POS: The simple UPOS part-of-speech tag.
Tag: The detailed part-of-speech tag.
Dep: Syntactic dependency, i.e. the relation between tokens.
Shape: The word shape – capitalization, punctuation, digits.
is alpha: Is the token an alpha character?
is stop: Is the token part of a stop list, i.e. the most common words of the language?
spacy.explain("VBZ")
"""


def named_entinty():
    url = "https://en.wikipedia.org/wiki/Tesla,_Inc."
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content div
    content = soup.find(id = "mw-content-text")

    # Extract text from paragraphs
    text = ''.join([p.get_text() for p in content.find_all('p')])
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            print(ent.text, ent.label_)



named_entinty()