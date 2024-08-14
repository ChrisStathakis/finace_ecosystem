import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("It was good, is is good times")

for token in doc:
    print(token.text)
    print(token.morph)
    print(token.morph.get("PronType"))
    print("--------------------")