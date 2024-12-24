import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import spacy

sent = '''
   I am reading a book., and in the next line, It is
    Python Machine Learning By Example,, then 2nd edition.
'''

tokens = word_tokenize(sent)
print(nltk.pos_tag(tokens))

porter_stemmer = PorterStemmer()
lemmarizer = WordNetLemmatizer()

print(lemmarizer.lemmatize("machines"), porter_stemmer.stem("machines"))
print(lemmarizer.lemmatize("learning"), porter_stemmer.stem("learning"))


print("--------------------------------------")
nlp = spacy.load("en_core_web_sm")
tokens2 = nlp(sent)
print([token.text for token in tokens2])
print([token.text for token in tokens2.ents])

# 57