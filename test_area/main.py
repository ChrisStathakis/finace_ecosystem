import spacy
# python -m spacy download en_core_web_sm

nlp = spacy.load("en_core_web_sm")

print("Pipeline: ", nlp.pipe_names)

doc = nlp("She was reading the paper.")
token = doc[2]

print(token.morph)
print("=================================================")
print(token.pos_)
print("=================================================")
print(token.morph.get("PronType"))